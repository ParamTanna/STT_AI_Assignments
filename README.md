# Software Tools & Techniques for AI — Assignments

An end-to-end tour of the modern **ML data lifecycle**, built across four assignments:
**acquire & validate → label → augment → train & deploy.** Each assignment is a
self-contained, runnable project; together they trace a dataset from raw web pages
all the way to a deployed prediction service.

> Course: *Software Tools & Techniques for AI* (2026). Completed as graded coursework.

---

## The lifecycle at a glance

| # | Project | Stage | Highlight |
|---|---------|-------|-----------|
| **1** | [Box-Office Bomb Data Pipeline](./Assignment-1) | Acquire & validate | Scraped 139 films, schema-validated with Pydantic, enriched via OMDb API |
| **2** | [Smart Labeling Pipeline](./Assignment-2) | Label | Human consensus (Fleiss' κ = 0.78), weak supervision, active learning, LLM labeling |
| **3** | [Multimodal Sentiment Engine](./Assignment-3) | Augment | Grew 328 → 677 samples; **+7 pts accuracy (76% → 83%)**; multilingual + audio |
| **4** | [PropTech Rent Predictor](./Assignment-4) | Train & deploy | Tuned RandomForest (MAE ₹12.4k), tracked with trackio, shipped on Streamlit + Docker |

---

## Assignment 1 — Box-Office Bomb Data Pipeline
*A robust ETL pipeline that turns a messy Wikipedia table into clean, validated, enriched data.*

- **Scraping:** parsed the Wikipedia "biggest box-office bombs" table (BeautifulSoup), handling nested headers and reference markers (139 films extracted).
- **Validation:** modeled records with **Pydantic** — custom field validators strip footnotes/symbols, coerce types, and average budget/loss ranges (e.g. `"$100–160"`).
- **Enrichment:** queried the **OMDb API** for plot, ratings, director, and language, gracefully handling `N/A` and API misses.
- **Consistency:** cross-checked Wikipedia vs. OMDb release years → 137/139 verified.

**Stack:** `requests` · `BeautifulSoup` · `Pydantic` · OMDb API

## Assignment 2 — Smart Labeling Pipeline
*A cost-effective labeling pipeline blending humans, rules, and LLMs.*

- **Human annotation:** measured inter-annotator agreement across 3 annotators — **Fleiss' Kappa = 0.78** (from-scratch implementation matches `statsmodels` exactly).
- **Weak supervision:** wrote Snorkel-style labeling functions and analyzed coverage / overlap / conflict.
- **Active learning:** prioritized the most informative samples to cut labeling budget.
- **LLM labeling:** bulk-labeled reviews via a few-shot prompt and ran a hallucination / noisy-label check against the gold standard.

**Stack:** `scikit-learn` · `Snorkel` · Label Studio · OpenRouter LLM API

## Assignment 3 — Multimodal Sentiment Engine
*Expanding a tiny labeled set into a large, diverse, multimodal, multilingual corpus — without human annotation.*

- **Classical augmentation:** WordNet synonym replacement + back-translation, with a Jaccard-similarity quality filter (123 new minority-class samples).
- **LLM synthesis:** generated 300 synthetic reviews (few-shot), measured diversity via **Self-BLEU** (~0.58–0.63) and filtered for sentiment consistency.
- **Multilingual:** English→Hindi→English round-trip with BLEU + sentiment-preservation checks.
- **Multimodal:** generated speech with gTTS, transcribed back with **Whisper** — mean **WER ≈ 0.06**.
- **Result:** final corpus of **677 samples** lifted black-box evaluator accuracy from **76% → 83%**.

**Stack:** `nltk` · `deep-translator` · `gTTS` · `openai-whisper` · `librosa` · `transformers`

## Assignment 4 — PropTech Rent Predictor
*Training, tuning, tracking, and deploying a rent-prediction model end-to-end.*

- **Modeling:** RandomForest regressor on ~13.9k Indian rental listings (Mumbai/Delhi/Pune/Hisar).
- **Hyperparameter search:** compared **Grid, Random, and Bayesian (Optuna)** search under 5-fold CV; best config = 200 trees, depth 25.
- **Tracking:** logged every search method, timing, and score with **trackio**; visualized trials-vs-error and the Optuna search space.
- **Deployment:** **Streamlit** app, containerized with **Docker**, deployed to **Hugging Face Spaces**.
- **Result:** test-set **MAE ≈ ₹12,417**.

🔗 **Live demo:** https://huggingface.co/spaces/yuvraj-rathod-1202/sttai_assignment4

**Stack:** `scikit-learn` · `Optuna` · `trackio` · `Streamlit` · `Docker`

---

## Running locally

Each assignment folder is independent. Typical flow:

```bash
cd Assignment-N
pip install -r requirements.txt      # where provided
# then open the notebook, or for A4:
streamlit run app.py
```

API-based assignments (1, 2, 3) read keys from environment variables — set
`OMDB_API_KEY` / `OPENROUTER_API_KEY` (e.g. in a `.env` file) before running.
No secrets are committed to this repo.
