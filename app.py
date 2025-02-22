import streamlit as st
import time
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyD7zV3BLjzdWbtMk9peFEsmkd3kUIMiQeY")

# Set page config
st.set_page_config(page_title="GenAI Code Fixer", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #F0F8FF;
        color: black;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .user-message {
        background-color: #007BFF;
        color: white;
        text-align: left;
    }
    .bot-message {
        background-color: #2E2E2E;
        color: white;
        text-align: left;
    }
    .button {
        background-color: #007BFF;
        color: white; 
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 10px; 
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Animated text function
def animated_text(text, speed=0.05):
    placeholder = st.empty()
    displayed_text = ""
    for letter in text:
        displayed_text += letter
        placeholder.markdown(
            f"""
            <h1 style="text-align:center; color: #007BFF;">✨ {displayed_text}</h1>
            """,
            unsafe_allow_html=True
        )
        time.sleep(speed)

# Display animated welcome text
animated_text("Welcome to GenAI Code Fixer!", speed=0.1)

# Function to get Gemini response
def get_gemini_response(prompt):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text if response.text else "⚠️ AI Error: Unable to generate response."

# Sidebar for branding and instructions
with st.sidebar:
    st.title("🤖 GenAI Code Fixer")
    st.markdown("**Powered by Gemini AI**")
    st.markdown("💡 *Submit your Python code for debugging and improvements!*\n\n✅ Bug detection\n✅ Code optimizations\n✅ Best practices suggestions")

# Code input area
user_code = st.text_area("🐞 Paste Your Python Code Here:", height=200)

# Function to Debug Code Using Gemini AI
def debug_code_with_gemini(code):
    prompt = f"Debug the following code and provide the corrected version:\n\n{code}"
    return get_gemini_response(prompt)

# Function to Generate Code Improvement Suggestions
def get_suggestions_with_gemini(code):
    prompt = f"Suggest improvements for the following code, focusing on best practices, efficiency, and readability:\n\n{code}"
    return get_gemini_response(prompt)

# Analyze Button with enhanced features
if st.button("🚀 Fix & Improve Code", key="analyze_button"):
    if user_code:
        with st.spinner("🛠️ Debugging your code..."):
            fixed_code = debug_code_with_gemini(user_code)
        
        with st.spinner("🔍 Generating suggestions..."):
            suggestions = get_suggestions_with_gemini(fixed_code)
        
        # Display Fixed Code
        st.subheader("✅ Debugged Code:")
        st.code(fixed_code, language="python")
        
        # Copy Button for Fixed Code
        st.download_button(
            label="📥 Download Fixed Code",
            data=fixed_code,
            file_name="fixed_code.py",
            mime="text/plain",
            help="Click to save the corrected code."
        )
        
        # Display AI-Generated Suggestions
        st.subheader("💡 Code Improvement Suggestions:")
        st.write(suggestions)
    else:
        st.warning("⚠️ Please enter some code before generating fixes and suggestions!")
