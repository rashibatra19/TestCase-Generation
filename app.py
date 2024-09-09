import streamlit as st
import base64
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_ollama.llms import OllamaLLM
# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini LLM client via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=google_api_key
)

# Function to encode image to base64
def encode_image_to_base64(file) -> str:
    return base64.b64encode(file.read()).decode('utf-8')

# Function to generate testing instructions using LLM
def generate_testing_instructions(context: str, screenshots: List[str], llm) -> str:
    prompt_template = PromptTemplate(
        input_variables=["text", "screenshots"],
        template=(
            "Here are examples of test case descriptions:\n\n"
            "1. *Test Case 1*: Check login functionality.\n"
            "   - *Pre-conditions*: User must have an active account.\n"
            "   - *Testing Steps*: Open the app, enter username and password, click login.\n"
            "   - *Expected Result*: User is directed to the dashboard.\n\n"
            "2. *Test Case 2*: Verify 'Forgot Password' functionality.\n"
            "   - *Pre-conditions*: User must have a registered email.\n"
            "   - *Testing Steps*: Click on 'Forgot Password', enter email, check inbox.\n"
            "   - *Expected Result*: User receives a password reset link.\n\n"
            "Based on these examples and the following step-by-step screenshots:\n\n"
            "{screenshots}\n\n"
            "And the provided context:\n\n"
            "{text}\n\n"
            "Create a detailed, step-by-step guide for testing each functionality described in the screenshots. For each test case, include:\n\n"
            "1. *Description*: What the test case is about.\n"
            "2. *Pre-conditions*: What needs to be set up or ensured before testing.\n"
            "3. *Testing Steps*: Clear, step-by-step instructions on how to perform the test.\n"
            "4. *Expected Result*: What should happen if the feature works correctly.\n\nGuide:"
        )
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run({"text": context, "screenshots": "\n".join(screenshots)})
    return result

# Streamlit UI configuration
st.set_page_config(page_title="Testing Instruction Generator", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container {
        background: #F0F2F6;
    }
    .sidebar .sidebar-content {
        background: #003366;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: #66CCFF;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #003366;
        color: white;
        border: None;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #00509E;
    }
    .stTextArea textarea, .stFileUploader {
        border: 2px solid #003366;
        border-radius: 5px;
    }
    .stAlert {
        border-color: #003366;
        background-color: #e8f4f8;
    }
    .stExpander>div {
        background-color: #003366;
        color: white;
    }
    .stExpander>div:hover {
        background-color: #00509E;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.title("Multimodal LLM Testing Instruction Generator")
st.markdown("""
    *Welcome to the Testing Instruction Generator!*
    This tool helps you create detailed, step-by-step testing instructions for digital product features based on your uploaded screenshots.
    - *Upload Screenshots:* Provide the images of the product features you want to test.
    - *Enter Context (optional):* Add any additional information to enhance the LLM’s understanding.
    - *Generate Instructions:* Click the button below to get a comprehensive guide on testing each functionality.
    """)

# Sidebar for optional context
with st.sidebar:
    st.header("Optional Context")
    context = st.text_area("Enter any additional context or information here...", height=200)
    st.markdown("Provide relevant details or instructions to help generate precise testing instructions.")

# Main layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Upload Screenshots")
    uploaded_files = st.file_uploader("Upload Screenshots (label each as Step 1, Step 2, etc.)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        st.write("Uploaded Screenshots:")
        screenshots = []
        for i, uploaded_file in enumerate(uploaded_files):
            img_base64 = encode_image_to_base64(uploaded_file)
            screenshots.append(f"Step {i+1}: ![Screenshot {i+1}](data:image/jpeg;base64,{img_base64})")
            st.image(uploaded_file, caption=f"Step {i+1}: {uploaded_file.name}", use_column_width=True)

with col2:
    st.header("Instructions")
    st.markdown("""
    - *Upload Screenshots:* Add screenshots of the digital product features you want to test.
    - *Enter Context (optional):* Provide additional context that might help in generating precise testing instructions.
    - *Click 'Describe Testing Instructions':* Get a detailed guide on how to test each functionality of the screenshots.
    """)

# Button to generate testing instructions
if st.button('Describe Testing Instructions'):
    if not uploaded_files:
        st.warning("Please upload at least one screenshot to generate testing instructions.")
    else:
        with st.spinner("Generating testing instructions..."):
            try:
                instructions = generate_testing_instructions(context, screenshots, llm)
                st.subheader("Generated Testing Instructions")
                st.write(instructions)
                st.download_button(
                    label="Download Testing Instructions",
                    data=instructions,
                    file_name="testing_instructions.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error generating testing instructions: {e}")

# Footer section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #003366;'>
        <p>Developed by Rashi Batra - AI Engineering Intern Challenge</p>
    </div>
""", unsafe_allow_html=True)