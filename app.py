import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Quality Dashboard", layout="wide")

# =========================
# CSS (FOR pH BAR + UI)
# =========================
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }

.ph-bar {
    height: 20px;
    border-radius: 10px;
    background: linear-gradient(to right, orange, lightgreen, purple);
    margin-bottom: 10px;
}

.ph-indicator {
    height: 10px;
    background-color: white;
    border-radius: 5px;
    margin-top: -15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("water_model.pkl")
scaler = joblib.load("scaler.pkl")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Water Input Panel")

water_type = st.sidebar.radio(
    "Select Water Type",
    ["Drinking", "Normal", "Industrial"]
)

ph = st.sidebar.slider("pH", 0.0, 14.0, 7.0, step=0.1)
hardness = st.sidebar.slider("Hardness", 0.0, 350.0, 200.0)
solids = st.sidebar.slider("Solids", 0.0, 60000.0, 15000.0, step=100.0)
chloramines = st.sidebar.slider("Chloramines", 0.0, 15.0, 7.0, step=0.1)
sulfate = st.sidebar.slider("Sulfate", 0.0, 500.0, 300.0)
conductivity = st.sidebar.slider("Conductivity", 0.0, 800.0, 400.0)
organic_carbon = st.sidebar.slider("Organic Carbon", 0.0, 30.0, 10.0, step=0.1)
trihalomethanes = st.sidebar.slider("Trihalomethanes", 0.0, 120.0, 60.0)
turbidity = st.sidebar.slider("Turbidity", 0.0, 10.0, 4.0, step=0.1)

# =========================
# MAIN UI
# =========================
st.title("Water Potability Prediction Dashboard")
st.write("Analyze water quality and determine if it is safe for drinking.")

# =========================
# pH VISUAL BAR 🔥
# =========================
st.subheader("pH Level Indicator")

st.markdown('<div class="ph-bar"></div>', unsafe_allow_html=True)

# position indicator (percentage)
ph_position = (ph / 14) * 100

st.markdown(
    f"""
    <div style="position: relative; width: 100%;">
        <div style="
            position: absolute;
            left: {ph_position}%;
            top: -18px;
            width: 10px;
            height: 25px;
            background: white;
            border-radius: 5px;">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(f"Current pH Value: **{ph}**")

if ph < 6.5:
    st.error("Acidic Water")
elif 6.5 <= ph <= 8.5:
    st.success("Safe pH Range")
else:
    st.warning("Alkaline Water")

# =========================
# PREDICTION
# =========================
if st.button("Run Prediction"):

    input_data = np.array([[ph, hardness, solids, chloramines,
                            sulfate, conductivity, organic_carbon,
                            trihalomethanes, turbidity]])

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0]

    # 🔥 LIGHT SAFETY LOGIC (BALANCED)
    unsafe_flag = False

    if ph < 6.5 or ph > 8.5:
        unsafe_flag = True
    if turbidity > 5:
        unsafe_flag = True
    if solids > 30000:
        unsafe_flag = True

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prediction Result")

        if prediction == 1 and not unsafe_flag:
            if water_type == "Drinking":
                st.success("Water is safe for drinking")
            elif water_type == "Normal":
                st.success("Water is safe for normal usage")
            else:
                st.success("Water is safe for industrial use")
        else:
            st.error("Water is NOT safe")

        confidence = round(max(prob)*100, 2)

        st.metric("Confidence Score", f"{confidence}%")
        st.progress(int(confidence))

        st.subheader("Simple Explanation")

        if unsafe_flag:
            st.write("Some parameters exceed safe limits.")
        elif prediction == 1:
            st.write("Water parameters are within acceptable range.")
        else:
            st.write("Model predicts unsafe based on learned patterns.")

    with col2:
        st.subheader("Probability Distribution")

        labels = ["Unsafe", "Safe"]

        fig, ax = plt.subplots()
        ax.bar(labels, prob)
        ax.set_title("Prediction Probability")

        st.pyplot(fig)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("Water Quality ML Dashboard | Streamlit App")
