import requests
import streamlit as st
import json

def login(username, password):
    """Login to the API and return the token."""
    url = "http://41.226.183.241:22032/api/auth/login"

    payload = {
        "username": username,
        "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response = response.json()
        response = response['data']['user']

        return response['jwt']
    else:
        raise Exception("Failed to login: {}".format(response.text))

# -----------------------------
# 🔹 Prediction Function (highest score)
# -----------------------------
def predict(
    project_id,
    instance,
    username,
    password 
):
    endpoint = "http://41.226.183.241:22032/api/projects/model/test/{projectId}"
    url = endpoint.replace("{projectId}", project_id)
    
    # 1. do login and get jwt token 
    token = login(username=username, password=password)
    
    # 2. prepare payload to be sent to the server
    payload = {
        "input": instance
    }
    
    # 3. prepare HTTP request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token),
    }
    
    # 4. send request to the server
    response = requests.post(url, headers=headers, json=payload)

    # 5. check if no server errors
    if response.status_code != 200:
        raise Exception("Request failed: {}".format(response.json()))
        
    # 6. parse the server response
    response = response.json()

    # 7. get the predictions from the response
    response = response['data']
    predictions = response['predictions']
    
    
    if len(predictions) == 0:
        # return empty array if there is no predictions
        return []
    else:
        return predictions


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
project_id = st.selectbox("Select Material", []) # put the list of projects here 
year = st.number_input("Year", min_value=2013, max_value=2025, value=2022)
month = st.number_input("Month", min_value=1, max_value=12, value=1)

# Prediction
if st.button("🔮 Predict Next Month's Price"):
    predictions = predict(
        project_id='', # your skeyepredict project_id
        instance='', # the constructed instance (in skeyepredict format)
        username='', # your skeyepredict username
        password='' # your skeyepredict password
    )
    
    if len(predictions) > 0:
        color_map = {
            "Very_Low": "🟦 Very Low",
            "Low": "🟩 Low",
            "Medium": "🟨 Medium",
            "High": "🟧 High",
            "Very_High": "🟥 Very High"
        }

        # Update the code 
        # st.success(f"📌 Prediction for **{material}** ({month}/{year} → {month+1}/{year}):")
        # st.markdown(f"<h2>{color_map.get(prediction, prediction)}</h2>", unsafe_allow_html=True)
        # st.info(get_recommendation(prediction))
    else:
        st.warning("⚠️ No prediction found in JSON.")

st.markdown("<hr><p style='text-align:center;'>🚀 Powered by <b>Uplify</b> | Smart Procurement Solutions</p>", unsafe_allow_html=True)
