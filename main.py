import streamlit as st
import json

# -----------------------------
# 🔹 Load JSON Models
# -----------------------------
def load_json_models():
    with open("cabling.json") as f:
        cabling_model = json.load(f)
    with open("cement.json") as f:
        cement_model = json.load(f)
    with open("rmc.json") as f:
        rmc_model = json.load(f)
    with open("timber.json") as f:
        timber_model = json.load(f)

    return {
        "Cabling": cabling_model,
        "Cement": cement_model,
        "Ready Mixed Concrete": rmc_model,
        "Timber": timber_model
    }

models = load_json_models()

# -----------------------------
# 🔹 Prediction Function (highest score)
# -----------------------------
def predict_category(material):
    model = models[material]
    best_prediction = None
    best_score = -1

    for rule_block in model["AggregatedRules"]:
        score = sum(rule["Score"] for rule in rule_block["Rules"]) / len(rule_block["Rules"])
        if score > best_score:
            best_score = score
            best_prediction = rule_block["Annotation"].replace("price:", "")

    return best_prediction

# -----------------------------
# 🔹 Recommendation Function
# -----------------------------
def get_recommendation(prediction):
    if prediction in ["High", "Very_High"]:
        return "🔺 Prices are expected to rise. Recommendation: **Buy now** to reduce costs."
    elif prediction in ["Low", "Very_Low"]:
        return "🔻 Prices are expected to drop. Recommendation: **Wait** before making large purchases."
    else:
        return "➖ Prices are stable. Recommendation: **Proceed with normal procurement**."

# -----------------------------
# 🔹 Streamlit App Layout
# -----------------------------
st.set_page_config(page_title="Uplify Procurement Predictor", layout="centered")

# Custom CSS to pin logo to far-left
st.markdown(
    """
    <style>
    .header-container {
        display: flex;
        align-items: center;
    }
    .header-container img {
        position: absolute;
        top: 20px;
        left: 20px;
        width: 200px; /* Bigger logo */
    }
    .header-text {
        margin-left: 240px; /* Push title to the right of the logo */
    }
    </style>
    <div class="header-container">
        <img src="uplify.png">
        <div class="header-text">
            <h1>🏗️ Building Material Price Predictor</h1>
            <p>Developed to support the <b>Procurement Department</b> in making data-driven purchase decisions.</p>
        </div>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# User inputs
st.subheader("📥 Select Parameters")
material = st.selectbox("Select Material", list(models.keys()))
year = st.number_input("Year", min_value=2013, max_value=2025, value=2022)
month = st.number_input("Month", min_value=1, max_value=12, value=1)

# Prediction
if st.button("🔮 Predict Next Month's Price"):
    prediction = predict_category(material)
    if prediction:
        color_map = {
            "Very_Low": "🟦 Very Low",
            "Low": "🟩 Low",
            "Medium": "🟨 Medium",
            "High": "🟧 High",
            "Very_High": "🟥 Very High"
        }

        st.success(f"📌 Prediction for **{material}** ({month}/{year} → {month+1}/{year}):")
        st.markdown(f"<h2>{color_map.get(prediction, prediction)}</h2>", unsafe_allow_html=True)
        st.info(get_recommendation(prediction))
    else:
        st.warning("⚠️ No prediction found in JSON.")

st.markdown("<hr><p style='text-align:center;'>🚀 Powered by <b>Uplify</b> | Smart Procurement Solutions</p>", unsafe_allow_html=True)
