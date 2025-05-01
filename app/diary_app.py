import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from google.cloud import firestore
import requests
from datetime import datetime, timedelta
from langchain.llms import OpenAI
from langchain_core.prompts import PromptTemplate
#from config import FIREBASE_KEY_PATH, HF_TOKEN
from utils.date_utils  import format_friendly_date
from utils.llm_api import query_chat

# Authenticate to Firestore with key
hf_token = st.secrets['HF_TOKEN']
key_path = st.secrets['FIREBASE_KEY_PATH']
db = firestore.Client.from_service_account_json(key_path)


st.title("My Diary App")


option = st.radio("What would you like to do?", ["New Entry", "Add Prior Entry"])

if option == "New Entry":
    # Add new diary entry
    entry = st.text_area("Enter your notes or write out what you did:")

    # Save Raw entry
    if st.button("Save Raw Entry"):
        doc_ref = db.collection("entries").document()
        doc_ref.set({
            "entry": entry,
            "date": datetime.now() # adds current date and time 
        })
        st.success("Raw entry saved!")
    
    # Generate diary entry with LLM
    if st.button("Generate Diary Entry"):
        prompt = ("Write a detailed, first-person diary entry based solely on the following notes:\n" + entry)
        generated_entry = query_chat(prompt)
        st.write("### Generated Diary Entry")
        st.write(generated_entry)

        # option to save generated entry
        if st.button("Save Generated Entry"):
            doc_ref = db.collection("entries").document()
            doc_ref.set({
                "entry": generated_entry,
                "date": datetime.now() # adds current date and time 
            })
            st.success("Generated diary entry saved!")
elif option == "Add Prior Entry":
    entry = st.text_area("Enter the prior diary entry:")
    date_input = st.date_input("Entry Date", value=datetime.now().date()) # default is today, streamlit widget calendar picker
    
    if st.button("Save Entry"):
        entry_date = datetime.combine(date_input, datetime.min.time()) # cuz firestore only accepts datetime bruh  
        doc_ref = db.collection("entries").document()
        doc_ref.set({
            "entry": entry,
            "date": entry_date # adds current date and time 
        })
        st.success("Prior entry added!")

# Display previous entries
st.subheader("Previous Entries")
display_option = st.radio("Display options:", ["Show All (Most Recent First)", "Filter by Date"])
entries = db.collection("entries").order_by("date", direction=firestore.Query.DESCENDING).stream()

if display_option == "Show All (Most Recent First)":

    for doc in entries:
        data = doc.to_dict()
        st.write(f"**{data.get('date').strftime('%b %d, %Y')}**: {data.get('entry')}")
else:
    # Filter by date options
    filter_option = st.selectbox("Filter by:", ["Last 7 days", "Last 3 months", "Custom Range"])

    # Filter by Last 7 days
    if filter_option == "Last 7 days":
        start_date = datetime.now().date() - timedelta(days=7)
        entries = db.collection("entries").where("date", ">=", datetime.combine(start_date, datetime.min.time())) \
                .order_by("date", direction=firestore.Query.DESCENDING).stream()
    
    # display entries in friendly format
    entry_count = 0
    for doc in entries:
        data = doc.to_dict()
        entry_date = data.get('date')
        formatted_date = format_friendly_date(entry_date)
        st.write(f"**{formatted_date}**: {data.get('entry')}")
        entry_count += 1
    
    if entry_count == 0:
        st.info("No entries found for the selected time period.")

