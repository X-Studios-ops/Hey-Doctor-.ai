import streamlit as st

st.set_page_config(
    page_title="Free BMI Calculator | HeyDoctor.ai"
)

st.title("⚖️ Free BMI Calculator")

height = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
weight = st.number_input("Weight (kg)", 10.0, 300.0, 70.0)

if st.button("Calculate BMI"):
    bmi = weight / ((height / 100) ** 2)

    st.success(f"Your BMI is {bmi:.2f}")

    if bmi < 18.5:
        st.warning("Underweight")
    elif bmi < 25:
        st.success("Normal")
    elif bmi < 30:
        st.warning("Overweight")
    else:
        st.error("Obese")

st.header("What is BMI?")

st.write("""
BMI (Body Mass Index) helps determine
whether your weight is healthy according
to your height.
""")
