import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Retrieve the API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key is not set. Please add it to your .env file.")
    st.stop()

# Initialize the Groq client
client = Groq(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="VENOM Q&A Chatbot")
st.header("VENOM: Hey, Let's Chat")

# Initialize session state for storing messages
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        {"role": "system", "content": "You are a comedian AI assistant"}
    ]


# Function to get response from Groq API
def get_groq_response(question):
    try:
        chat_completion = client.chat.completions.create(
            messages=st.session_state['flowmessages'] + [{"role": "user", "content": question}],
            model="llama3-8b-8192",
        )
        answer = chat_completion.choices[0].message.content
        st.session_state['flowmessages'].append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        st.error(f"API request failed: {e}")
        return "Error in response generation."


# Display conversation history
st.subheader("Conversation History")
for message in st.session_state['flowmessages']:
    if message['role'] == 'user':
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**VENOM:** {message['content']}")

# Chat input and response handling
message = st.chat_input("Say your doubts to VENOM")

if message:
    # Print user message to console for logging/debugging
    print(f"User Input: {message}")

    # Add user message to the conversation history
    st.session_state['flowmessages'].append({"role": "user", "content": message})

    # Get the response from the Groq API
    response = get_groq_response(message)

    # Display VENOM's response
    st.subheader("You Says...")
    st.write(message)
    st.subheader("VENOM Says...")
    st.write(response)
