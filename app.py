import streamlit as st
from backend import hash_data, query_llama, simulate_progress

# Apply custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    body {
        font-family: 'Poppins', Arial, sans-serif;
        background: linear-gradient(120deg, #fdfbfb, #ebedee);
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #3498db;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    h2, h3, h4 {
        color: #2c3e50;
    }
    .btn-primary {
        background: linear-gradient(90deg, #56ab2f, #a8e063);
        color: white;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    .btn-primary:hover {
        background: linear-gradient(90deg, #a8e063, #56ab2f);
        transform: scale(1.05);
        cursor: pointer;
    }
    .progress-bar > div {
        width: 0%;
        animation: progress-animation 2s ease-out forwards;
    }
    @keyframes progress-animation {
        to {
            width: 100%;
        }
    }
    footer {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #666;
    }
    footer a {
        color: #3498db;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Streamlit app
st.title("🌟 TalentScout: Hiring Assistant Chatbot")
st.markdown(
    "Welcome to **TalentScout's Hiring Assistant**! I’m here to guide you through the screening process with a few simple steps. Let’s get started! 😊"
)

# Show a progress bar for flow tracking
progress = st.progress(0)

# Initialize session state for tracking conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "step" not in st.session_state:
    st.session_state.step = 0

# Step 0: Collect Candidate Details
if st.session_state.step == 0:
    st.subheader("Candidate Details")
    name = st.text_input("👤 Full Name:", placeholder="Enter your full name").strip()
    email = st.text_input("📧 Email Address:", placeholder="Enter your email").strip()
    phone = st.text_input("📞 Phone Number:", placeholder="Enter your phone number").strip()
    experience = st.text_input("💼 Years of Experience:", placeholder="E.g., 3 years").strip()
    position = st.text_input("🎯 Desired Position(s):", placeholder="E.g., Data Scientist").strip()
    location = st.text_input("📍 Current Location:", placeholder="E.g., San Francisco").strip()
    tech_stack = st.text_area(
        "🛠️ Tech Stack (programming languages, frameworks, tools):",
        placeholder="E.g., Python, TensorFlow, AWS"
    ).strip()

    if st.button("Submit"):
        # Validate if any field is empty
        if not name or not email or not phone or not experience or not position or not location or not tech_stack:
            st.error("Please fill in all the fields before submitting!")
        else:
            anonymized_name = f"Candidate-{hash_data(name)}"
            anonymized_email = f"anon-{hash_data(email)}@example.com"
            anonymized_phone = f"+XXXXXXX-{phone[-4:]}"
            st.session_state.conversation.extend([
                {"role": "user", "content": f"My name is {anonymized_name}"},
                {"role": "user", "content": f"My anonymized email is {anonymized_email}, my anonymized phone is {anonymized_phone}"},
                {"role": "user", "content": f"I have {experience} years of experience."},
                {"role": "user", "content": f"I am applying for the position(s): {position}."},
                {"role": "user", "content": f"My current location is {location}."},
                {"role": "user", "content": f"My tech stack includes {tech_stack}."},
            ])

            st.write(f"Thank you for sharing your details, {anonymized_name}! 😊")
            st.write("Analyzing your expertise and generating questions...")

            # Simulate progress bar
            with st.spinner("Processing..."):
                simulate_progress()

            # Proceed to the next step
            st.session_state.step = 1
            progress.progress(50)

# Step 1: Generate Technical Questions
if st.session_state.step == 1:
    response = query_llama(
        st.session_state.conversation
        + [{"role": "user", "content": f"Generate 3-5 technical questions for {tech_stack}, focusing on {experience} years of experience"}]
    )

    if response:
        if "Unexpected error occurred" in response or "issue processing your request" in response:
            st.warning("The chatbot could not generate questions based on the input. Please refine the details and try again.")
        else:
            st.subheader("Personalized Technical Questions")
            st.write(response)
            st.session_state.step = 2
            progress.progress(100)
    else:
        st.error("Failed to generate questions. Please try again.")
        st.session_state.step = 0

# Step 2: Final Steps
if st.session_state.step == 2:
    st.subheader("Final Steps")
    st.write("Thank you for providing all the required details! We’ll review your profile and get back to you soon. 😊")
    if st.button("End Conversation"):
        st.write("Conversation ended. Have a great day!")
        st.session_state.step = 0
        progress.progress(0)

# Footer
st.markdown(
    """
    <footer>
        © 2025 TalentScout. All rights reserved.</a>
    </footer>
    """,
    unsafe_allow_html=True,
)
