import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel

# Configure Google Generative AI SDK with your API Key
genai.configure(api_key="AIzaSyD-m3NL82BiGJF2oAxOT-awnPP-gRZe-8k")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to handle chatbot conversation using Gemini model
def get_response(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are a chatbot designed to offer financial assistance in the Indian context. "
                    "You will only respond to queries related to savings, investments, or finance. "
                    "If a user asks about something unrelated to finance, politely respond with 'I can only assist with finance, savings, or investments. Please ask questions in that domain.' "
                    "Ask the user for their savings in Indian Rupees, and based on the amount they provide, "
                    "give detailed investment strategies, including suggestions for Recurring Deposits (RD), Fixed Deposits (FD), "
                    "Systematic Investment Plans (SIPs), mutual funds, stock market investments, bonds, and any other relevant options."
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Hello! I am your Financial Assistant. How much have you saved in rupees? I can help you make smart investment decisions based on that."
                ],
            }
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text

# Function to display chat history and get user input
def chatbot_interface():
    # Initialize session state for chat history and input
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            "Bot: Hello! I am your Financial Assistant. How much have you saved in rupees?"
        ]

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Display chat history
    for chat in st.session_state.chat_history:
        st.text(chat)

    # User input text box
    user_input = st.text_input("You:", key="input", value=st.session_state.user_input)

    # Button to send message and get a response
    st.markdown('<div class="chat-buttons">', unsafe_allow_html=True)
    if st.button("Send"):
        if user_input.strip():
            # Append user's message to chat history
            st.session_state.chat_history.append(f"You: {user_input}")
            
            # Get chatbot response and append it to chat history
            bot_response = get_response(user_input)
            st.session_state.chat_history.append(f"Bot: {bot_response}")
            
            # Clear the input for next user input
            st.session_state.user_input = ""

    # Button to start a new chat
    if st.button("New Chat"):
        st.session_state.chat_history = [
            "Bot: Hello! I am your Financial Assistant. How much have you saved in rupees?"
        ]
        st.session_state.user_input = ""
    st.markdown('</div>', unsafe_allow_html=True)

# Function to show saving recommendations and launch chatbot
def show_saving_recommendations():
    st.markdown("<h2 style='text-align: center;'>Saving Recommendations</h2>", unsafe_allow_html=True)

    # Display chatbot interface when user clicks "Start Chatbot"
    chatbot_interface()

    # Add 'Back to Dashboard' button
    st.markdown('<div class="back-to-dashboard-button">', unsafe_allow_html=True)
    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
