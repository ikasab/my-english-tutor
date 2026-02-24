import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽", layout="centered")

# --- CUSTOM CSS (Дизайн) ---
st.markdown("""
    <style>
    /* Главный фон и шрифт */
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Стиль карточки */
    .event-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #007bff;
        transition: transform 0.2s;
    }
    .event-card:hover {
        transform: translateY(-5px);
    }
    
    /* Красивые заголовки */
    .main-title {
        color: #1E1E1E;
        text-align: center;
        font-weight: 700;
        margin-bottom: 30px;
    }
    
    /* Индикатор мест */
    .seats-badge {
        background-color: #e1f5fe;
        color: #01579b;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# Инициализация данных
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.markdown("<h1 class='main-title'>⚽ სპორტული შეხვედრები</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ТАБ 1: КРАСИВЫЙ СПИСОК ---
with tab1:
    if not st.session_state.events:
        st.info("თამაშები ჯერ არ არის. შექმენი პირველი!")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
