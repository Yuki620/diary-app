import requests
import streamlit as st
import openai

openai.api_key = st.secrets['GROQ_TOKEN']
openai.api_base = "https://api.groq.com/openai/v1"

def query_chat(prompt):
    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",  # or "mixtral-8x7b-32768"
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


# API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-0.5B-Chat"
# headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

# def query_hf_chat(prompt):
#     payload = {
#         "inputs": prompt
#     }
#     response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
#     print("Status Code:", response.status_code)
#     print("Raw Response:", response.text)

#     # Attempt to decode JSON
#     try:
#         return response.json()
#     except Exception as e:
#         return {"error": f"Failed to decode JSON — possibly model failed or unauthorized. Details: {response.text}"}
#     result = response.json()

#     # some models generate results as list 
#     if isinstance(result, list) and "generated_text" in result[0]:
#         return result[0]["generated_text"]
#     # some models generate results as dictionary
#     if "generated_text" in result:
#         return result["generated_text"]
    
   

