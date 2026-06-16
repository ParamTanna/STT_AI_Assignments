# Assignment 4: PropTech Startup Strategy - Rent Prediction Pipeline

[HF Spaces Demo](https://huggingface.co/spaces/yuvraj-rathod-1202/sttai_assignment4)

## What To Run

This project has two steps:

1. Run [train.ipynb](train.ipynb) to preprocess the dataset, tune the model, and generate the pickle artifacts in `models/`.
2. Run [app.py](app.py) with Streamlit, or build the Docker image and run the container.

The web app expects these generated files to exist:

- `models/best_rf_model.pkl`
- `models/city_encoder.pkl`
- `models/location_encoder.pkl`
- `models/property_type_encoder.pkl`
- `models/status_encoder.pkl`

## Local Run

```bash
streamlit run app.py
```

## Docker Run

```bash
docker build -t sttai-a4 .
docker run -p 8501:8501 sttai-a4
```