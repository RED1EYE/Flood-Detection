import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import langchain_groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv("D:\coding\python\.env")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LangChain Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are SAHAS, a disaster alert assistant. Provide precise information about flood."),
    ("user", "Question: {question}")
])

# Initialize Groq LLM
llm = ChatGroq(model="llama3-70b-8192")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit Page Configuration
st.set_page_config(page_title="SAHAS - Hazard Alert System", page_icon="⚠️", layout="wide")

# Custom CSS for Dark Mode
dark_mode_css = """
    <style>
    /* Global dark mode background */
    body, .stApp {
        background-color: #121212 !important;
        color: #FFFFFF !important;
    }

    /* Sidebar background */
    .stSidebar, .css-1lcbmhc, .css-1d391kg, .css-qrbaxs {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }

    /* Chat container & assistant response */
    .stMarkdown, .stChatMessage, .css-1aumxhk {
        background-color: #222 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    /* Input text box */
    .stTextInput>div>div>input {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 10px !important;
    }

    /* Send button */
    .stButton>button {
        background-color: #444 !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Title section */
    .stHeader {
        background-color: #121212 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #222;
    }
    ::-webkit-scrollbar-thumb {
        background: #666;
        border-radius: 10px;
    }
    </style>
"""



# Sidebar
st.sidebar.markdown("## Settings")

# Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.sidebar.button("Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply Dark Mode if enabled
if st.session_state.dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
    
# Custom Navigation
st.title("SAHAS - Satellite Assisted Hazard Alert System")
st.sidebar.markdown("## Select Model")
model_options = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
selected_model = st.sidebar.selectbox("Groq Model", model_options)

# Update Model
if st.sidebar.button("Update Model"):
    llm = ChatGroq(model=selected_model)
    chain = prompt | llm | output_parser
    st.sidebar.success(f"Model updated to {selected_model}")

# Chat Interface
st.markdown("### SAHAS Assistant")

# Store chat messages
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?", "timestamp": datetime.now().strftime("%H:%M %p")}]

# Display chat history
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "assistant" else "user"
    st.markdown(f"**{role.capitalize()}**: {msg['content']}  \n*{msg['timestamp']}*")

# User input field
user_input = st.text_input("Ask about disaster risks in your area...")
if st.button("Send"):
    if user_input:
        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now().strftime("%H:%M %p")})

        # Send input to Groq API and get response
        with st.spinner("Generating response..."):
            try:
                response = chain.invoke({'question': user_input})
                st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": datetime.now().strftime("%H:%M %p")})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}", "timestamp": datetime.now().strftime("%H:%M %p")})
        
        # Refresh chat
        
