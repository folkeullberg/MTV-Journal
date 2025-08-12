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
    st.markdown("<h1 style='text-align: center;'>Välkommen till MTV-JOURNAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Snabb och enkel journalhantering för dig i sjukvården</p>", unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Skriv ditt lösenord", label_visibility="collapsed")
    if st.button("Logga in", use_container_width=True):
        if password == "journal123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Fel lösenord. Försök igen.")
else:
    # Full-screen layout
    st.markdown("<style> section[data-testid='stSidebar'] { display: none !important; } .block-container { padding: 1rem; } .main { max-width: 100vw; } </style>", unsafe_allow_html=True)
    
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

    # Main layout: Phrases (left), large note (center), categories (right)
    col_left, col_center, col_right = st.columns([2, 4, 1])
    
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
            key = f"phrase_{phrase}_{uuid.uuid4()}"
            selected = st.session_state.selected_phrases.get(phrase, False)
            button_style = "background-color: #4CAF50; color: white;" if selected else ""
            st.markdown(f"<style>button[kind='secondary'][key='{key}'] {{ {button_style} font-size: 18px; height: 50px; }}</style>", unsafe_allow_html=True)
            if st.button(phrase, key=key, use_container_width=True):
                if not selected:
                    if phrase in ["Filtek Supreme XTE", "Filtek One", "Filtek Supreme"]:
                        color = st.selectbox("", ["A1", "A2", "A3", "B1", "B2"], label_visibility="collapsed")
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