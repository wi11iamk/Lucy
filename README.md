# Alma: A Dementia-Friendly AI Companion

## Why Alma?

As people age, some experience cognitive decline that affects their ability to communicate and remember important details. Caregivers and family members often struggle to provide continuous support while ensuring their loved ones remain engaged and safe. 

**Alma** is designed as a **conversational AI companion** to help dementia patients feel more connected while giving caregivers tools to track changes in communication patterns.

---

## What Alma Does

Engage in **clear, simple, and supportive conversations**  
Track **changes in speech patterns** over time  
Ensure **AI-generated responses are safe and appropriate**  
Protect **patient data** and prevent unauthorized access  

---

## Installation

Install dependencies before running Alma:

```bash
pip install transformers spacy cryptography numpy
python -m spacy download en_core_web_sm
```

---

## How to Use

### **Running Alma**
Clone the repository:
```bash
git clone https://github.com/your-repo/alma-ai-companion.git
cd alma-ai-companion
```

Run the main script:
```bash
python main.py
```

Example Output:
```
AI Response: That sounds interesting! Tell me more.
Cognitive Report: Speech patterns stable
Encrypted Log: gAAAAABj... (Encrypted data)
```

---

## Project Structure
```
alma_ai_companion/
│── main.py                  # Main execution file
│── config.py                # Configuration settings
│── response_engine.py       # Generates dementia-friendly responses
│── speech_analysis.py       # Monitors speech patterns
│── safety_monitor.py        # Checks for unsafe AI responses
│── security.py              # Encrypts data and manages access
│── auth.py                  # Handles user authentication
│── utils.py                 # Helper functions
│── models/                  # Stores pre-trained LLM models
│── logs/                    # Stores safety reports and patient logs
│── database/                # Secure encrypted data storage
```

---

## Future Plans
- **Speech-to-Text Support** for voice interactions.
- **Long-Term Memory Recall** for more personalized conversations.
- **Advanced NLP Models** for improved engagement.

---

## Considerations
- **Data Security**: Patient logs are encrypted and access is restricted.  
- **Responsible AI**: Responses are designed to be **clear and non-misleading**.  
- **Caregiver Support**: Alma is **not a replacement for human care** but a tool to assist caregivers.

---

## Contributions
If you're interested in improving Alma, feel free to submit a pull request or open an issue.

**Maintainers**: `@wi11iamk`
