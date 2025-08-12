# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import uuid

st.set_page_config(layout="wide")

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
            st.rerun()
        else:
            st.error("Fel lösenord")
else:
    # Custom CSS for Apple-like styling
    st.markdown("""
    <style>
        .stApp { background-color: #F2F2F7; max-width: 100vw; margin: 0; padding: 0; overflow: hidden; }
        .block-container { padding: 1rem 2rem; max-width: 100%; }
        div [data-testid="baseButton-secondary"] { background-color: #007AFF; color: white; border-radius: 10px; border: none; font-size: 18px; min-height: 50px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        div [data-testid="baseButton-secondary"]:hover { background-color: #0066CC; }
        div.stTextArea > div > div > textarea { background-color: white; border-radius: 10px; border: 1px solid #CED3D9; font-size: 16px; min-height: 70vh; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stExpander { background-color: transparent; border: none; box-shadow: none; }
    </style>
    """, unsafe_allow_html=True)

    # Minimal header with discrete buttons
    col_left_header, col_right_header = st.columns([1, 10])
    with col_left_header:
        admin_expander = st.expander("⚙️", expanded=False)
        with admin_expander:
            admin_action = st.radio("", ["Ny kategori", "Ny fras"])
            if admin_action == "Ny kategori":
                new_category = st.text_input("", placeholder="Kategorinamn", label_visibility="collapsed")
                if st.button("Lägg till"):
                    if new_category:
                        st.session_state.sections[new_category] = []
                        save_data(st.session_state.sections)
                        st.success("Tillagd!")
                        st.rerun()
            else:
                category = st.selectbox("", list(st.session_state.sections.keys()), label_visibility="collapsed")
                new_phrase = st.text_input("", placeholder="Fras", label_visibility="collapsed")
                if st.button("Lägg till"):
                    if new_phrase:
                        st.session_state.sections[category].append(new_phrase)
                        save_data(st.session_state.sections)
                        st.success("Tillagd!")
                        st.rerun()
    with col_right_header:
        if st.button("Logga ut"):
            st.session_state.logged_in = False
            st.session_state.note = []
            st.session_state.selected_phrases = {}
            st.rerun()

    # Main layout: phrases (left), large note (center), categories (right)
    col_left, col_center, col_right = st.columns([2, 5, 1])
    
    # Categories (right, simple list)
    with col_right:
        for section in st.session_state.sections.keys():
            if st.button(section, key=f"sec_{section}", use_container_width=True):
                st.session_state.current_section = section
                st.session_state.selected_phrases = {}
                st.rerun()

    # Phrases (left, large buttons with green select)
    with col_left:
        phrases = st.session_state.sections[st.session_state.current_section]
        for phrase in phrases:
            phrase_key = f"phrase_{phrase}"
            selected = st.session_state.selected_phrases.get(phrase, False)
            if selected:
                st.markdown(f"<style>div [data-testid=\"baseButton-secondary\"][key='{phrase_key}'] {{ background-color: #34C759; }}</style>", unsafe_allow_html=True)
            if st.button(phrase, key=phrase_key, use_container_width=True):
                if not selected:
                    if phrase in ["Filtek Supreme XTE", "Filtek One", "Filtek Supreme"]:
                        color = st.selectbox("", ["A1", "A2", "A3", "B1", "B2"], label_visibility="collapsed", key=f"color_{phrase}")
                        st.session_state.note.append(f"{phrase}, färg {color}")
                    else:
                        st.session_state.note.append(phrase)
                    st.session_state.selected_phrases[phrase] = True
                else:
                    st.session_state.note = [p for p in st.session_state.note if not p.startswith(phrase)]
                    st.session_state.selected_phrases[phrase] = False
                st.rerun()

    # Large note area (center)
    with col_center:
        note_text = f"{st.session_state.current_section}:\n" + "\n".join(st.session_state.note) if st.session_state.note else "Börja med att välja fraser."
        st.text_area("", note_text, height=500, label_visibility="collapsed")
        col_copy, col_clear = st.columns(2)
        with col_copy:
            if st.button("Kopiera", use_container_width=True):
                st.markdown(f"<script>navigator.clipboard.writeText('{note_text.replace('\\', '\\\\').replace('\'', '\\\'').replace('\n', '\\n')}')</script>", unsafe_allow_html=True)
                st.success("Kopierad!")
        with col_clear:
            if st.button("Rensa", use_container_width=True):
                st.session_state.note = []
                st.session_state.selected_phrases = {}
                st.rerun()