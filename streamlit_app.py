#from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

#load_dotenv()  # Loading all the environment variables from .env file

#api_key = os.getenv("GOOGLE_API_KEY")  # Accessing the environment variables
api_key=st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)  # Loading the API key into the generativeai module

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Pro Chatbot")
st.header("Gemini Flash Chatbot")

input = st.text_input("Ask me anything")
submit = st.button("Generate Response")

if submit:
    response = get_gemini_response(input)
    st.write(response)
