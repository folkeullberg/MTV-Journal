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

# Login page
if not st.session_state.logged_in:
    st.title("MTV-JOURNAL - Logga in")
    password = st.text_input("Lösenord", type="password")
    if st.button("Logga in"):
        if password == "journal123":  # Simple shared password
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Fel lösenord")
else:
    # Main app
    st.title("MTV-JOURNAL")

    # Admin section (gear icon simulated with a button)
    with st.expander("⚙️ Admininställningar", expanded=False):
        st.subheader("Hantera kategorier och fraser")
        admin_action = st.radio("Välj åtgärd", ["Lägg till huvudkategori", "Lägg till fras"], key="admin_action")

        if admin_action == "Lägg till huvudkategori":
            new_category = st.text_input("Ny huvudkategori", key="new_category")
            if st.button("Lägg till kategori", key="add_category"):
                if new_category and new_category not in st.session_state.sections:
                    st.session_state.sections[new_category] = []
                    save_data(st.session_state.sections)
                    st.success(f"Kategori '{new_category}' tillagd!")
                    st.rerun()

        elif admin_action == "Lägg till fras":
            category = st.selectbox("Välj kategori att lägga till fras i", list(st.session_state.sections.keys()), key="category_for_phrase")
            new_phrase = st.text_input("Ny fras", key="new_phrase")
            if st.button("Lägg till fras", key="add_phrase"):
                if new_phrase and new_phrase not in st.session_state.sections[category]:
                    st.session_state.sections[category].append(new_phrase)
                    save_data(st.session_state.sections)
                    st.success(f"Fras '{new_phrase}' tillagd i '{category}'!")
                    st.rerun()

    # Section selection
    st.subheader("Välj sektion")
    section = st.selectbox("Sektion", list(st.session_state.sections.keys()), key="section_select")
    st.session_state.current_section = section

    # Add phrases
    st.subheader(f"Fraser för {section}")
    phrases = st.session_state.sections[section]
    for phrase in phrases:
        if st.button(phrase, key=f"phrase_{phrase}_{uuid.uuid4()}"):
            if phrase in ["Filtek Supreme XTE", "Filtek One", "Filtek Supreme"]:
                color = st.selectbox("Välj färg", ["A1", "A2", "A3", "B1", "B2"], key=f"color_{phrase}_{uuid.uuid4()}")
                st.session_state.note.append(f"{phrase}, färg {color}")
            else:
                st.session_state.note.append(phrase)

    # Display and copy note
    if st.session_state.note:
        st.subheader("Sammanfattad anteckning")
        note_text = f"{section}:\n" + "\n".join(st.session_state.note)
        st.text_area("Kopiera denna text:", note_text, height=200)
        if st.button("Rensa anteckning"):
            st.session_state.note = []
            st.rerun()

    # Logout
    if st.button("Logga ut"):
        st.session_state.logged_in = False
        st.rerun()