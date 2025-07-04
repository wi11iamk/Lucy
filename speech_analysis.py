import spacy
import numpy as np

nlp = spacy.load("en_core_web_sm")

baseline_sentence_lengths = [7, 9, 8, 10]


def analyze_speech_patterns(text):
    doc = nlp(text)
    sentence_lengths = [len(sent.text.split()) for sent in doc.sents]

    avg_length = np.mean(sentence_lengths)
    decline_flag = avg_length < (np.mean(baseline_sentence_lengths) - 2)

    return (
        "Possible cognitive decline detected"
        if decline_flag
        else "Speech patterns stable"
    )
