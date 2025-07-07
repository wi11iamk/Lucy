FROM python:3.11-slim

# env hygiene
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TOKENIZERS_PARALLELISM=false \
    HUGGING_FACE_HUB_DISABLE_TELEMETRY=1

WORKDIR /app

COPY requirements.lock ./
RUN pip install --upgrade pip \
    && pip install --extra-index-url https://download.pytorch.org/whl/cpu \
         -r requirements.lock \
    && python -m spacy download en_core_web_sm

COPY . /app

CMD ["python", "main.py"]