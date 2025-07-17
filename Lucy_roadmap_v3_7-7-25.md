
# Lucy – Product & Engineering Roadmap  *(revision 2025-07-07)*

---

## 1 Personas & Jobs‑to‑Be‑Done

| Persona | Key problems | Lucy’s promised outcome |
|---------|--------------|-------------------------|
| **Person with mild–moderate dementia** | • Social isolation • Anxiety when memory lapses • Trouble conveying needs | • Compassionate chat adapted to cognitive state • Grounding reminders & reminiscence prompts |
| **Family caregiver** | • Wants early warning of decline • Peace of mind while away | • Dashboard with language‑trend charts & safety alerts • Secure profile editor |
| **Clinician / researcher** | • Sparse visit data • Compliance hurdles | • Exportable, de‑identified language metrics • API hook for research |

---

## 2 MVP Feature Set

| Pillar | Feature | Status |
|--------|---------|--------|
| Conversational core | Dementia‑tuned system prompt; emotion reflection | **Done** (needs severity selector) |
| Safety & security | Prompt‑injection guard, constitutional filter, RBAC, Fernet | **Done** |
| Longitudinal insights | Sentence & emotion drift plots (SQLite‑backed) | Baseline done |
| Personal profile | Caregiver‑editable likes, life events, media library | **Planned** |
| Caregiver console | Streamlit/FastAPI dashboard | **Planned** |
| Data portability | CSV/Parquet export, OAuth share | **Planned** |
| Deployment | Docker image (+ tablet build) | **Done** |
| Compliance guardrails | Audit log, consent flag, retention | **Design** |

---

## 3 Technical Architecture (tablet MVP)

```text
┌─────────────────────────────┐
│ Streamlit UI (/chat /admin) │
└─────────────┬───────────────┘
              │ REST
┌─────────────▼────────────┐     (optional)────────┐
│ FastAPI Gateway          │───► Redis (rate‑limit)│
│  • AuthZ (PIN)           │                       │
│  • Logging → SQLite      │◄──────────────────────┘
└─────────────┬────────────┘
              │ gRPC
┌─────────────▼───────────────────────────┐
│ response_engine (HF models + OpenAI)    │
│  • Whisper‑small ASR (local)            │
│  • Emotion & sentiment classifiers      │
│  • RAG on patient_profile embeddings    │
└──────────────────────────────────────────┘
```
*Primary store = **SQLite** file `lucy.db` (encrypted).  
Cloud deployment will swap to **PostgreSQL** simply by changing `DATABASE_URL`; ORM code is unchanged.*

---

## 4 Patient‑Profile Data Model

| Table | Purpose |
|-------|---------|
| **BioFact** | Key‑value preferences (name, pronouns, pets) |
| **LifelineEvent** | Date‑stamped life milestones |
| **Interest** | Tag + MiniLM embedding |
| **CarePlan** | Agitation trigger → intervention URI |
| **AllowedMedia** | Whitelisted media files/links |

---

## 5 Language‑based Cognitive Metrics

| Feature family | Example metric | Lib |
|----------------|----------------|-----|
| Lexical diversity | Type‑token ratio | spaCy |
| Syntactic complexity | Dependency depth | spaCy |
| Fluency | Words‑per‑minute, pause freq | pyannote |
| Coherence | SBERT cosine drift | sentence‑transformers |
| LM perplexity | GPT‑2 perplexity baseline | transformers |

Nightly batch writes `Interaction.cognitive_score` (z‑score vs baseline).

---

## 6 Milestone Plan (6‑week cadence)

| Sprint | Deliverable | Metric |
|--------|-------------|--------|
| **0.1** *(done)* | CI, Docker, baseline plots | Green on PRs |
| **0.2** | SQLite persistence (done) + lexical metric batch | History survives restart |
| **0.3** | FastAPI service (`/chat`, `/metrics`) | JSON responses in docker‑compose |
| **0.4** | Streamlit caregiver dashboard + profile editor | Caregiver can view weekly flags & edit profile |
| **0.5** | Export & consent flows, staging deploy (Fly) | Pilot with 2 families |
| **1.0 beta** | Hardened auth, monitoring, offline ASR fallback | Pilot with 5 families |

---

## 7 Sprint 0.2 – Engineering Task List _(updated)_

| ID | Task | Est |
|----|------|-----|
| **DB‑CLEAN** | Remove legacy JSONL writer & folder | 0.25 d |
| **ALG‑01** | Nightly lexical‑metric batch → `cognitive_score` | 2 d |
| **RAG‑01** | Embed `Interest` rows; inject top‑k into prompts | 0.5 d |
| **TEST‑01** | Persistence test: restart app → history intact | 0.5 d |
| **DOC‑01** | `docs/arch.md` architecture diagram | 0.5 d |

*Removed MIG‑01 (JSONL importer) as no longer needed.*

---

## 8 Open Discussion Points

* Consent & data‑sharing UX (toggle log, export)  
* Accessibility: voice output, high‑contrast mode  
* Multilingual support (spaCy `xx_sent_ud_sm`)  
* Clinical validation partnerships (compare cognitive_score to MMSE)
