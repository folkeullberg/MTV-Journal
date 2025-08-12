# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import uuid

# File for persistent storage
DATA_FILE = "journal_data.json"

# Initialize or load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "Compositfyllning": [
            "Excavering",
            "Preparation",
            "Ets med fluorvätesyra",
            "Bonding: Prime&Bond Universal",
            "Filtek Supreme XTE",
            "Filtek One",
            "Filtek Supreme",
            "Puts & polering",
            "Postop info"
        ]
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "note" not in st.session_state:
    st.session_state.note = []
if "sections" not in st.session_state:
    st.session_state.sections = load_data()
if "current_section" not in st.session_state:
    st.session_state.current_section = "Compositfyllning"
if "selected_phrases" not in st.session_state:
    st.session_state.selected_phrases = {}

# Welcoming login page
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #007AFF;'>Välkommen till MTV-JOURNAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #6E6E6E;'>Snabb journalhantering för dig i vården</p>", unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Lösenord", label_visibility="collapsed")
    if st.button("Logga in", use_container_width=True):
        if password == "journal123":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Fel lösenord")
else:
    # Full-screen Apple-like design with light colors
    st.markdown("""
        <style>
            .reportview-container { max-width: 100vw; padding: 0; background-color: #F2F2F7; }
            .main { max-width: 100vw; padding: 0; }
            button { background-color: #007AFF; color: white; font-size: 18px; height: 50px; border-radius: 10px; }
            button:active { background-color: #0056B3; }
            .selected-button { background-color: #34C759; color: white; }
            .stTextArea textarea { background-color: white; border-radius: 10px; font-size: 16px; height: 60vh; }
            .stExpander { border: none; }
            .st