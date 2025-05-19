import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Check if the API key is available
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables.")
    st.stop()

# Configure Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

# Initialize session state for conversation flow if not already initialized
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        {"role": "model", "parts": [{"text":"You are an expert Data Structures and Algorithms assistant and answer only when you are 100 percent sure. "
                    "Whenever a user inputs a piece of code, analyze it and explain the underlying DSA approach or algorithm used. "
                    "Focus only on explaining the approach, time complexity, and relevant data structures. "
                    "Do not provide the full code solution or unrelated information."}]}  # Replaced "content" with "parts"
    ]

# Function to get response from Gemini API
def get_gemini_response(question):
    # Append user's message to conversation flow
    st.session_state['flowmessages'].append({"role": "user", "parts": [{"text": question}]})  # Use "parts"

    # Prepare message format as expected by Gemini API
    message_parts = []
    for msg in st.session_state['flowmessages']:
        message_parts.append({
            "role": msg["role"],
            "parts": msg["parts"]
        })

    # Initialize the chat model for the session
    chat = genai.GenerativeModel("gemini-1.5-flash")
    chat_history = message_parts  # Update with proper structure

    # Send message to Gemini API
    try:
        response = chat.start_chat(history=chat_history).send_message(question)
        # Extract and return response from the chat model
        answer = response.text
        st.session_state['flowmessages'].append({"role": "model", "parts": [{"text": answer}]})  # Model sends the response
        return answer
    except Exception as e:
        st.error(f"Error: {e}")
        return f"Error: Unable to get response from Gemini API. Details: {str(e)}"

# Streamlit input and button for user interaction
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Handle the submit button click
if submit and input:
    response = get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)

elif submit:
    st.warning("Please enter a question before submitting.")

# Display conversation history
st.subheader("Conversation History:")
for msg in st.session_state['flowmessages']:
    st.write(f"**{msg['role'].capitalize()}:** {msg['parts'][0]['text']}")
