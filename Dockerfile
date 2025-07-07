FROM python:3.11-slim

# env hygiene
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TOKENIZERS_PARALLELISM=false \
    HUGGING_FACE_HUB_DISABLE_TELEMETRY=1

WORKDIR /app
COPY . /app

# Install build deps for spaCy model, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && pip install --upgrade pip \
    && pip install -r requirements.lock \
    && python -m spacy download en_core_web_sm \
    && apt-get purge -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]