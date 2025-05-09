import joblib
import streamlit as st
import math as math
import numpy as np

st.title("Stellar Classification App 🌟")
st.write("Enter the stellar parameters to get the classification:")

# Load the trained model
model=joblib.load('stellarClassificationModel.pkl')
# Input fields
bv = st.number_input("Enter B-V Value:")
luminosity = st.number_input("Enter Luminosity:")
magnitude_option = st.selectbox(
    "Do you have the Absolute Magnitude?",
    ("Yes", "No")
)

# If the user has absolute magnitude, ask for it
if magnitude_option == "Yes":
    magnitude = st.number_input("Enter Absolute Magnitude:", value=0.0)

# If the user doesn't have absolute magnitude, ask for Parallax and Apparent Magnitude
else:
    parallax = st.number_input("Enter Parallax:", value=0.0)
    app_mag = st.number_input("Enter Apparent Magnitude:", value=0.0)

    # Calculate Absolute Magnitude only if parallax is greater than 0
    if parallax > 0:
        magnitude = app_mag + 5 * math.log10(parallax / 100.0)

temperature = 4600*((1/((0.92*bv)+1.7))+(1/((0.92*bv)+0.62)))
radius = ((((luminosity*3.828*(10**26))/(4*math.pi*5.67*(10**-8)*(temperature**4)))**(1/2))/(6.95*(10**8)))
if luminosity!=0:
  age = 10*(luminosity**-0.7)

# Predict button
if st.button("Classify Star"):
    try:
        # Prediction
        features = [[bv,temperature,luminosity,radius,magnitude,age]]
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities) * 100
        st.write(f"### Predicted Stellar Type: {prediction}")
        st.write(f"### Confidence Score: {confidence:.2f}%")

    except Exception as e:
        st.write("Error occurred:", e)
