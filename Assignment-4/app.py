import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="UrbanNest Rent Predictor", layout="wide")

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parent


def load_pickle(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(f"Missing required artifact: {model_path}")
    with model_path.open("rb") as model_file:
        return pickle.load(model_file)

@st.cache_resource
def load_artifacts():
    city_encoder = load_pickle(BASE_DIR / "models" / "city_encoder.pkl")
    location_encoder = load_pickle(BASE_DIR / "models" / "location_encoder.pkl")
    property_encoder = load_pickle(BASE_DIR / "models" / "property_type_encoder.pkl")
    status_encoder = load_pickle(BASE_DIR / "models" / "status_encoder.pkl")
    model = load_pickle(BASE_DIR / "models" / "best_rf_model.pkl")
    return city_encoder, location_encoder, property_encoder, status_encoder, model
try:
    # ---------------- LOAD ENCODERS + MODEL ----------------
    city_encoder, location_encoder, property_encoder, status_encoder, model = load_artifacts()
except FileNotFoundError:
    st.set_page_config(page_title="UrbanNest Rent Predictor", layout="wide")
    st.title("🏠 UrbanNest Rent Predictor")
    st.error("Model artifacts are missing. Run train.ipynb first to generate the encoder and model pickle files in the models/ folder.")
    st.code("jupyter notebook train.ipynb", language="bash")
    st.stop()

# ---------------- SESSION STATE ----------------
if "prediction" not in st.session_state:
    st.session_state.prediction = None

# ---------------- TITLE ----------------
st.title("🏠 UrbanNest Rent Predictor")
st.caption("Enter property details to estimate rent")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Property Inputs")

location = st.sidebar.selectbox("Location", location_encoder.classes_)
city = st.sidebar.selectbox("City", city_encoder.classes_)

latitude = st.sidebar.number_input("Latitude", value=19.0760, step=0.000001, format="%.6f")
longitude = st.sidebar.number_input("Longitude", value=72.8777, step=0.000001, format="%.6f")

numBathrooms = st.sidebar.slider("Bathrooms", 1, 10, 2)
numBalconies = st.sidebar.slider("Balconies", 0, 5, 1)

isNegotiable_ui = st.sidebar.radio("Negotiable", ["No", "Yes"])
isNegotiable = 1 if isNegotiable_ui == "Yes" else 0

SecurityDeposit = st.sidebar.number_input("Security Deposit", step=1000)

Status = st.sidebar.selectbox("Furnishing Status", status_encoder.classes_)

Size_ft2 = st.sidebar.number_input("Size (sq ft)", step=50, value=200)

BHK_ui = st.sidebar.radio("Type", ["BHK", "RK"])
BHK = 1 if BHK_ui == "BHK" else 0

rooms_num = st.sidebar.slider("Number of Rooms", 1, 10, 2)

property_type = st.sidebar.selectbox("Property Type", property_encoder.classes_)

verification_days = st.sidebar.number_input("Days Since Posted")

# ---------------- BUTTON ----------------
st.sidebar.markdown("---")
predict_clicked = st.button("Predict Rent")

if predict_clicked:

    if Size_ft2 <= 0:
        st.error("⚠️ Size must be greater than 0")

    else:
        with st.spinner("Predicting rent..."):
            time.sleep(1)

            # ---------------- ENCODING ----------------
            city_enc = city_encoder.transform([city])[0]
            location_enc = location_encoder.transform([location])[0]
            property_enc = property_encoder.transform([property_type])[0]
            status_enc = status_encoder.transform([Status])[0]

            # ---------------- CREATE DATAFRAME ----------------
            input_data = pd.DataFrame([{
                "location": location_enc,
                "city": city_enc,
                "latitude": latitude,
                "longitude": longitude,
                "numBathrooms": numBathrooms,
                "numBalconies": numBalconies,
                "isNegotiable": isNegotiable,
                "SecurityDeposit": SecurityDeposit,
                "Status": status_enc,
                "Size_ft²": Size_ft2,
                "BHK": BHK,
                "rooms_num": rooms_num,
                "property_type": property_enc,
                "verification_days": verification_days
            }])

            # ---------------- PREDICTION ----------------
            prediction = model.predict(input_data)

            st.session_state.prediction = int(prediction[0])

# ---------------- RESULT ----------------
if st.session_state.prediction is not None:

    col_main, col_side = st.columns([1, 1])

    with col_main:
        st.subheader("Estimated Rent")
        st.markdown(f"### ₹ {st.session_state.prediction:,}")

    with col_side:
        st.subheader("Property Specifications")
        st.write("**Rooms :**", rooms_num)
        st.write("**Bathrooms :**", numBathrooms)
        st.write("**Balconies :**", numBalconies)
        st.write("**Furnishing :**", Status)
        st.write("**Property Type :**", property_type)
        st.write("**Type :**", BHK_ui)
        st.write("**Size :**", f"{Size_ft2} sq ft")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Location Details")
        st.write("**Location :**", location)
        st.write("**City :**", city)
        st.write("**Coordinates :**", f"{latitude}, {longitude}")

    with col2:
        st.subheader("Features & Financials")
        st.write("**Negotiable :**", isNegotiable_ui)
        st.write("**Security Deposit :**", f"₹ {SecurityDeposit:,}")
        st.write("**Days Since Posted :**", verification_days)