# ML Data Lifecycle Pipeline

An end-to-end machine learning pipeline developed as part of the **Software Tools & Techniques for AI (2026)** course. The repository is organized into four independent modules that collectively demonstrate the complete ML workflow—from collecting raw data to deploying a trained model.

**Pipeline:** Data Acquisition & Validation → Data Labeling → Data Augmentation → Model Training & Deployment

---

## Repository Overview

| Module       | Focus                         | Key Outcome                                                                                           |
| ------------ | ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Module 1** | Data Acquisition & Validation | Scraped and validated 139 movie records, enriched using the OMDb API                                  |
| **Module 2** | Data Labeling                 | Combined human annotation, weak supervision, active learning, and LLM-assisted labeling               |
| **Module 3** | Data Augmentation             | Expanded a sentiment dataset from 328 to 677 samples and improved evaluation accuracy from 76% to 83% |
| **Module 4** | Model Training & Deployment   | Built, tuned, tracked, and deployed a rent prediction model                                           |

---

# Module 1 — Data Acquisition & Validation

Built an ETL pipeline that converts a semi-structured Wikipedia table into a clean, validated dataset.

### Features

* Scraped the Wikipedia page listing the biggest box-office bombs using BeautifulSoup.
* Parsed complex HTML tables containing nested headers and citation markers, extracting information for **139 films**.
* Defined data models using **Pydantic** with custom validators to:

  * remove footnotes and formatting artifacts,
  * convert values into consistent data types,
  * average budget and loss ranges (e.g. `$100–160M`).
* Enriched each record using the **OMDb API**, retrieving metadata such as plot, director, language, and ratings.
* Cross-validated release years between Wikipedia and OMDb, successfully matching **137 out of 139** records.

**Tech Stack:** Python, Requests, BeautifulSoup, Pydantic, OMDb API

---

# Module 2 — Data Labeling

Implemented multiple labeling strategies to create high-quality labeled data while reducing manual effort.

### Features

* Measured agreement among three human annotators using **Fleiss' Kappa (κ = 0.78)** with a from-scratch implementation validated against `statsmodels`.
* Designed Snorkel-style labeling functions and analyzed:

  * coverage,
  * overlap,
  * conflicts between labeling rules.
* Applied active learning to identify the most informative samples for manual annotation.
* Used few-shot prompting through an LLM to generate labels and evaluated label quality against the gold standard.

**Tech Stack:** Python, Scikit-learn, Snorkel, Label Studio, OpenRouter API

---

# Module 3 — Data Augmentation

Expanded a small sentiment dataset using multiple augmentation techniques while maintaining label quality.

### Features

* Applied classical augmentation using WordNet synonym replacement and back-translation with Jaccard similarity filtering.
* Generated **123 additional minority-class samples** through rule-based augmentation.
* Produced **300 synthetic reviews** using few-shot prompting and evaluated diversity with **Self-BLEU (~0.58–0.63)**.
* Performed multilingual augmentation using English ↔ Hindi translation with BLEU and sentiment consistency checks.
* Generated speech using **gTTS** and transcribed it with **Whisper**, achieving an average **WER ≈ 0.06**.
* Increased dataset size from **328 to 677 samples**, improving evaluation accuracy from **76% to 83%**.

**Tech Stack:** NLTK, Transformers, Whisper, gTTS, Deep Translator, Librosa

---

# Module 4 — Model Training & Deployment

Built and deployed a complete machine learning workflow for predicting rental prices.

### Features

* Trained a **Random Forest Regressor** on approximately **13.9k Indian rental listings** covering Mumbai, Delhi, Pune, and Hisar.
* Compared **Grid Search**, **Random Search**, and **Bayesian Optimization (Optuna)** using 5-fold cross-validation.
* Logged experiments, execution times, and evaluation metrics using **trackio**.
* Visualized optimization progress and search-space exploration.
* Containerized the application with Docker and deployed a Streamlit interface on Hugging Face Spaces.
* Achieved a final **test MAE of approximately ₹12,417**.

**Live Demo:** https://huggingface.co/spaces/yuvraj-rathod-1202/sttai_assignment4

**Tech Stack:** Scikit-learn, Optuna, Trackio, Streamlit, Docker

---

# Running the Projects

Each module is independent and can be executed separately.

```bash
cd Module-N
pip install -r requirements.txt
```

For Module 4:

```bash
streamlit run app.py
```

Modules that use external APIs read credentials from environment variables.

Required variables include:

* `OMDB_API_KEY`
* `OPENROUTER_API_KEY`

No API keys or secrets are committed to this repository.
