import openai
import json
import datetime
from transformers import pipeline
from config import OPENAI_API_KEY, SENTIMENT_MODEL, EMOTION_MODEL, FEW_SHOT_EXAMPLES, LOG_FILE_PATH

# Set OpenAI API key from config
openai.api_key = OPENAI_API_KEY

# Load pre-trained models using the configuration
sentiment_model = pipeline("sentiment-analysis")
emotion_model = pipeline(
    "text-classification",
    model=EMOTION_MODEL,
    return_all_scores=True
)

def analyze_emotion(user_input):
    """
    Analyze the user input to extract emotion scores.
    Returns a dictionary with emotions and their scores.
    """
    predictions = emotion_model(user_input)
    emotion_scores = {pred['label'].lower(): pred['score'] for pred in predictions[0]}
    return emotion_scores

def build_prompt_with_examples(user_input, emotion_scores, few_shot_examples=FEW_SHOT_EXAMPLES):
    """
    Build a prompt for the LLM that includes the user input, the emotion analysis,
    and optionally a set of few-shot examples.
    """
    emotion_summary = ", ".join(f"{emotion}: {score:.2f}" for emotion, score in emotion_scores.items())
    prompt = (
        "You are a compassionate assistant with expertise in dementia care. "
        "Your goal is to provide an empathetic and thoughtful response to the user's message.\n\n"
        f"User Input: \"{user_input}\"\n"
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
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        top_p=0.95,
        n=1,
        stop=None,
    )
    
    generated_text = response.choices[0].text.strip()
    return generated_text, emotion_scores, prompt

def log_interaction(user_input, emotion_scores, prompt, llm_response, log_file=LOG_FILE_PATH):
    """
    Log the details of the interaction for future reference and fine-tuning.
    Logs are appended to a JSON Lines file.
    """
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user_input": user_input,
        "emotion_scores": emotion_scores,
        "prompt": prompt,
        "llm_response": llm_response
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
