# AR_Thoughts_App.py

import streamlit as st
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

st.set_page_config(page_title="AR.Thoughts – Memory & Present Card Builder", layout="centered")

DATA_FILE = "card_storage.json"
PDF_FILE = "generated_card.pdf"

def save_to_json(data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)

    with open(DATA_FILE, "w") as f:
        json.dump(existing, f, indent=4)

def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def generate_pdf(card_data):
    c = canvas.Canvas(PDF_FILE, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 100, f"{card_data['Type']} CARD")
    c.setFont("Helvetica", 12)

    lines = [
        f"Who: {card_data['Who']}",
        f"What: {card_data['What']}",
        f"When: {card_data['When']}",
        f"Where: {card_data['Where']}",
        f"Senses: {', '.join(card_data['Senses'])}",
        f"Emotion: {card_data['Emotion']}",
        f"Belief: {card_data['Belief']}"
    ]

    y = height - 150
    for line in lines:
        c.drawString(100, y, line)
        y -= 25

    c.showPage()
    c.save()

# App Title
st.title("🧠 AR.Thoughts")
st.subheader("Build vivid character scenes — one memory or moment at a time.")

# Card Type Selector
card_type = st.radio("Choose card type:", ["Memory", "Present Moment"])

st.markdown("---")

# Shared Form Inputs
with st.form("card_form"):
    st.write(f"### {card_type} Card Details")

    who = st.text_input("Who is involved?")
    what = st.text_area("What happened?")
    when = st.text_input("When did it happen?")
    where = st.text_input("Where did it happen?")

    st.markdown("**Five Senses**")
    senses = st.multiselect("Select any that apply:", ["Smell", "Touch", "Taste", "Sight", "Sound"])

    emotion = st.text_input("Emotion (primary)")
    belief = st.text_input("Belief formed (if any)")

    submitted = st.form_submit_button("Generate Card")

# Display the card preview
if submitted:
    card = {
        "Type": card_type,
        "Who": who,
        "What": what,
        "When": when,
        "Where": where,
        "Senses": senses,
        "Emotion": emotion,
        "Belief": belief
    }

    st.markdown("### 🧩 Your Card")
    st.markdown(f"**Type:** {card_type}")
    st.markdown(f"**Who:** {who}")
    st.markdown(f"**What:** {what}")
    st.markdown(f"**When:** {when}")
    st.markdown(f"**Where:** {where}")
    st.markdown(f"**Five Senses:** {', '.join(senses)}")
    st.markdown(f"**Emotion:** {emotion}")
    st.markdown(f"**Belief:** {belief}")

    save_to_json(card)
    generate_pdf(card)

    with open(PDF_FILE, "rb") as pdf_file:
        st.download_button("📥 Download PDF", data=pdf_file, file_name=PDF_FILE)

# Load Existing Cards
if st.checkbox("📚 Show saved cards"):
    saved = load_cards()
    if saved:
        for idx, card in enumerate(saved[::-1], 1):
            st.markdown(f"**{idx}. {card['Type']} – {card['What'][:40]}...**")
            st.markdown(f"↪️ *{card['Emotion']}* | *{card['Belief']}*")
    else:
        st.info("No cards saved yet.")
