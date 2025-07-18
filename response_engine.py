import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline
from db.session import SessionLocal
from db.models import Interaction
from lucy_rag import fetch_topk, mark_used

from config import SENTIMENT_MODEL, EMOTION_MODEL, FEW_SHOT_EXAMPLES

# -------------------------------------------------
load_dotenv()
client = OpenAI()

pathlib.Path("logs").mkdir(exist_ok=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load pre-trained models using the configuration

sentiment_model = pipeline(
    "sentiment-analysis",
    model=SENTIMENT_MODEL,
)
emotion_model = pipeline(
    "text-classification",
    model=EMOTION_MODEL,
    top_k=None,  # replaces return_all_scores=True
)


def analyze_emotion(user_input):
    """
    Analyze the user input to extract emotion scores.
    Returns a dictionary with emotions and their scores.
    """
    predictions = emotion_model(user_input)
    emotion_scores = {pred["label"].lower(): pred["score"] for pred in predictions[0]}
    return emotion_scores


def build_prompt_with_examples(
    user_input, emotion_scores, few_shot_examples=FEW_SHOT_EXAMPLES
):
    """
    Build a prompt for the LLM that includes the user input, the emotion analysis,
    and optionally a set of few-shot examples.
    """

    emotion_summary = ", ".join(
        f"{emotion}: {score:.2f}" for emotion, score in emotion_scores.items()
    )
    mem_block = ""
    with SessionLocal() as db:
        memories = fetch_topk(db, k=3)
        if memories:
            mem_block = (
                "Patient memories:\n" + "\n".join(f"- {m}" for m in memories) + "\n\n"
            )
            for tag in memories:
                mark_used(tag, db)
            db.commit()

    prompt = (
        "You are a compassionate assistant with expertise in dementia care. "
        "Your goal is to provide an empathetic and thoughtful response to the user's message.\n\n"
        f'User Input: "{user_input}"\n'
        f"Emotion Analysis: {emotion_summary}\n\n"
    )
    if few_shot_examples:
        prompt += "Here are a few examples of ideal responses:\n"
        for example in few_shot_examples:
            prompt += (
                f"Input: \"{example['input']}\" | "
                f"Emotion: {example['emotion_summary']}\n"
                f"Response: {example['response']}\n\n"
            )

    prompt = mem_block + prompt
    prompt += (
        "Based on the above, generate a response that acknowledges the emotional state "
        "of the user and offers comfort and understanding."
    )
    return prompt


def generate_response_with_llm(user_input, few_shot_examples=FEW_SHOT_EXAMPLES):
    """
    Generate an LLM response based on the user input and emotion scores,
    optionally using few-shot examples.
    Returns the generated response, the emotion scores, and the full prompt.
    """
    emotion_scores = analyze_emotion(user_input)
    prompt = build_prompt_with_examples(user_input, emotion_scores, few_shot_examples)

    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # or "gpt-4o-mini" etc.
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
        top_p=0.95,
    )

    generated_text = chat_response.choices[0].message.content.strip()
    return generated_text, emotion_scores, prompt


def log_interaction(user_input, emotion_scores, prompt, llm_response):
    with SessionLocal() as db:
        db.add(
            Interaction(
                user_id="local",  # or actual user id
                user_input=user_input,
                llm_response=llm_response,
                emotion_scores=emotion_scores,
                safety_flag="⚠️" in llm_response,
            )
        )
        db.commit()
