import streamlit as st
import datetime
import pandas as pd
import uuid

# Set page config
st.set_page_config(page_title="Hospital Appointment System", page_icon="🏥")

# Sample data
departments = {
    "Cardiology": ["Dr. Smith", "Dr. Johnson"],
    "Neurology": ["Dr. Brown", "Dr. Davis"],
    "Pediatrics": ["Dr. Martinez", "Dr. Lee"]
}

# In-memory appointments DataFrame
if 'appointments_df' not in st.session_state:
    st.session_state.appointments_df = pd.DataFrame(columns=[
        "Appointment ID", "Name", "Age", "Department", "Doctor", "Date", "Time"
    ])

# AI advice function with expanded logic
def get_ai_advice(symptom):
    symptom = symptom.lower()
    if "fever" in symptom:
        return "You may have an infection. Drink fluids, rest, and monitor your temperature. Seek care if persistent."
    elif "headache" in symptom:
        return "Try rest, hydration, and avoid screen time. See a doctor if it's severe or recurrent."
    elif "chest pain" in symptom:
        return "Chest pain could be serious. Seek emergency medical attention immediately."
    elif "cough" in symptom:
        return "Persistent cough may indicate infection or irritation. If it's dry or productive for more than a week, consult a doctor."
    elif "fatigue" in symptom:
        return "Fatigue can be caused by stress, poor sleep, or medical conditions. Consider a check-up if persistent."
    elif "diarrhea" in symptom:
        return "Stay hydrated. If it lasts more than 2 days or includes blood, seek medical help."
    elif "sore throat" in symptom:
        return "It may be viral. Gargle with warm salt water and stay hydrated. See a doctor if painful or persistent."
    elif "nausea" in symptom:
        return "Eat light, stay hydrated. If vomiting continues, medical attention may be needed."
    elif "rash" in symptom:
        return "Could be allergic or infectious. Avoid irritants. If spreading or painful, consult a doctor."
    else:
        return "Symptom not recognized. Please consult a healthcare provider."

# Title
st.title("🏥 Hospital Appointment & AI Health Advice System")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["Book Appointment", "View Appointments", "Get AI Health Advice", "About"])

# Menu Option: Book Appointment
if menu == "Book Appointment":
    st.subheader("📅 Book a Doctor's Appointment")

    with st.form("appointment_form"):
        name = st.text_input("Your Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        department = st.selectbox("Choose Department", list(departments.keys()))
        doctor = st.selectbox("Select Doctor", departments[department])
        date = st.date_input("Select Date", min_value=datetime.date.today())
        time = st.time_input("Select Time")
        submitted = st.form_submit_button("Book Appointment")

        if submitted:
            if not name.strip():
                st.error("Name is required.")
            elif age <= 0:
                st.error("Please enter a valid age.")
            elif not department or not doctor or not date or not time:
                st.error("All fields must be filled.")
            else:
                appointment_id = str(uuid.uuid4())[:8]
                new_appointment = {
                    "Appointment ID": appointment_id,
                    "Name": name,
                    "Age": age,
                    "Department": department,
                    "Doctor": doctor,
                    "Date": str(date),
                    "Time": str(time)
                }

                st.session_state.appointments_df = pd.concat([
                    st.session_state.appointments_df,
                    pd.DataFrame([new_appointment])
                ], ignore_index=True)

                st.success(f"✅ Appointment booked! Your ID is: `{appointment_id}`")

# Menu Option: View Appointments
elif menu == "View Appointments":
    st.subheader("📋 Your Booked Appointments")
    if st.session_state.appointments_df.empty:
        st.info("No appointments booked yet.")
    else:
        st.dataframe(st.session_state.appointments_df)

# Menu Option: AI Health Advice
elif menu == "Get AI Health Advice":
    st.subheader("🤖 AI Health Advice Assistant")
    symptom = st.text_input("Describe your symptom (e.g., sore throat, nausea, fatigue)")
    if st.button("Get Advice"):
        if symptom.strip():
            advice = get_ai_advice(symptom)
            st.info(advice)
        else:
            st.error("❌ Please enter a symptom.")

# Menu Option: About
elif menu == "About":
    st.subheader("ℹ️ About This App")
    st.markdown("""
    This is a simple hospital interface built with **Streamlit**.

    **Features**:
    - Book doctor appointments with unique ID
    - View appointments in a table
    - Get AI-powered health tips for common symptoms

    _Note: This is a demo, not a substitute for real medical advice._
    """)
