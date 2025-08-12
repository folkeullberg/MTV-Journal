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

# Login page
if not st.session_state.logged_in:
    st.title("MTV-JOURNAL - Logga in")
    st.markdown("**Ange lösenord för att fortsätta**")
    password = st.text_input("Lösenord", type="password", placeholder="Skriv journal123")
    if st.button("Logga in", key="login_button", help="Klicka för att logga in"):
        if password == "journal123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Fel lösenord! Försök igen.")
else:
    # Main app layout with columns
    st.title("MTV-JOURNAL")
    col1, col2 = st.columns([3, 1])  # Main content (left), sidebar (right)

    # Logout button (top right)
    with col2:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("Logga ut", key="logout_button"):
            st.session_state.logged_in = False
            st.session_state.note = []
            st.session_state.selected_phrases = {}
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Admin settings (top left)
    with col1:
        with st.expander("⚙️ Admininställningar", expanded=False):
            st.markdown("**Hantera kategorier och fraser**")
            admin_action = st.radio("Välj åtgärd", ["Lägg till huvudkategori", "Lägg till fras"], key="admin_action")
            if admin_action == "Lägg till huvudkategori":
                new_category = st.text_input("Ny huvudkategori", placeholder="Skriv kategorinamn", key="new_category")
                if st.button("Lägg till kategori", key="add_category"):
                    if new_category and new_category not in st.session_state.sections:
                        st.session_state.sections[new_category] = []
                        save_data(st.session_state.sections)
                        st.success(f"Kategori '{new_category}' tillagd!")
                        st.rerun()
            elif admin_action == "Lägg till fras":
                category = st.selectbox("Välj kategori", list(st.session_state.sections.keys()), key="category_for_phrase")
                new_phrase = st.text_input("Ny fras", placeholder="Skriv fras", key="new_phrase")
                if st.button("Lägg till fras", key="add_phrase"):
                    if new_phrase and new_phrase not in st.session_state.sections[category]:
                        st.session_state.sections[category].append(new_phrase)
                        save_data(st.session_state.sections)
                        st.success(f"Fras '{new_phrase}' tillagd i '{category}'!")
                        st.rerun()

    # Sidebar with category list (right)
    with col2:
        st.markdown("**Välj kategori**")
        for section in st.session_state.sections.keys():
            if st.button(section, key=f"section_{section}_{uuid.uuid4()}", help=f"Välj {section}"):
                st.session_state.current_section = section
                st.rerun()

    # Main content: Phrases and note
    with col1:
        st.markdown(f"**Fraser för {st.session_state.current_section}**")
        phrases = st.session_state.sections[st.session_state.current_section]
        for phrase in phrases:
            # Initialize selected state for each phrase
            if phrase not in st.session_state.selected_phrases:
                st.session_state.selected_phrases[phrase] = False
            # Button with green highlight if selected
            button_style = "background-color: #90EE90;" if st.session_state.selected_phrases[phrase] else ""
            if st.button(phrase, key=f"phrase_{phrase}_{uuid.uuid4()}", help=f"Lägg till {phrase}", use_container_width=True):
                if not st.session_state.selected_phrases[phrase]:
                    if phrase in ["Filtek Supreme XTE", "Filtek One", "Filtek Supreme"]:
                        color = st.selectbox("Välj färg", ["A1", "A2", "A3", "B1", "B2"], key=f"color_{phrase}_{uuid.uuid4()}")
                        st.session_state.note.append(f"{phrase}, färg {color}")
                    else:
                        st.session_state.note.append(phrase)
                    st.session_state.selected_phrases[phrase] = True
                else:
                    st.session_state.note = [p for p in st.session_state.note if not p.startswith(phrase)]
                    st.session_state.selected_phrases[phrase] = False
                st.rerun()

    # Live note display and copy button (right)
    with col2:
        st.markdown("**Din anteckning**")
        if st.session_state.note:
            note_text = f"{st.session_state.current_section}:\n" + "\n".join(st.session_state.note)
            st.text_area("Kopiera denna text:", note_text, height=200, key="note_area")
            if st.button("Kopiera anteckning", key="copy_button", help="Kopiera texten till urklipp"):
                st.write("<script>navigator.clipboard.writeText(document.getElementById('note_area').value)</script>", unsafe_allow_html=True)
                st.success("Text kopierad!")
        else:
            st.text_area("Kopiera denna text:", "Ingen anteckning än. Klicka på fraser för att börja!", height=200, key="note_area_empty")
        if st.button("Rensa anteckning", key="clear_button"):
            st.session_state.note = []
            st.session_state.selected_phrases = {}
            st.rerun()