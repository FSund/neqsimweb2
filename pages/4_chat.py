import streamlit as st
import openai
from openai import OpenAI
#client = OpenAI()

API_KEY = st.secrets["apipas"]
OpenAI.api_key = API_KEY
client = OpenAI(api_key=API_KEY)

def make_request(question_input: str):
    try:
        completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=question_input,
        max_tokens=200,
        temperature=0
        )
        return completion.choices[0].text
    except:
        return ""
    
st.question = make_request
test = make_request("what is neqsim")
st.write(test)
