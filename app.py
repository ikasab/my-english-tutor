import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽", layout="centered")

# Данные в сессии
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

# Дизайн (CSS)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #007bff !important; 
        color: white !important; 
    }
    .event-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 6px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ სპორტული პლატფორმა")

# Вкладки
tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ВКЛАДКА 1: СПИСОК ИГР ---
with tab1:
    st.subheader("აქტიური თამაშები")
    if not st.session_state.events:
        st.info("თამაშები არ არის. შექმენი პირველი!")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            
            # Используем простые блоки вместо f-строк с HTML, чтобы избежать SyntaxError
            with st.container(border=True):
                st.markdown(f"### {event['sport']} — {event['place']}")
                st.write(f"📅 {event['date']} | ⏰ {event['time']}")
                st.markdown(f"**👥 მონაწილეები: {event['confirmed']}/{event['max_people']}**")
                
                if event['confirmed'] < event['max_people']:
                    if st.button(f"ჩაწერა (ID: {real_idx})", key=f"join_{real_idx}", use_container_width=True):
                        st.session_state.requests.append({
                            'event_id': real_idx, 
                            'user': f"მოთამაშე_{random.randint(10,99)}", 
                            'status': 'pending'
                        })
                        st.toast("მოთხოვნა გაიგზავნა!")
                else:
                    st.error("ადგილები შევსებულია")

# --- ВКЛАДКА 2: СОЗДАНИЕ ИГРЫ ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    with st.container(border=True):
        sport_in = st.selectbox("სპორტის სახეობა", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
        place_in = st.text_input("ჩატარების ადგილი", placeholder="მაგალითად: ვაკის პარკი")
        c1, c2 = st.columns(2)
        date_in = c1.date_input("თარიღი")
        time_in = c2.time_input("დრო")
        max_p_in = st.slider("მოთამაშეების მაქს. რაოდენობა", 2, 22, 10)
        
        if st.button("გამოქვეყნება 🚀", use_container_width=True):
            if place_in:
                st.session_state.events.append({
                    'sport': sport_in, 
                    'place': place_in, 
                    'date': str(date_in), 
                    'time': str(time_in), 
                    'max_people': max_p_in, 
                    'confirmed': 1
                })
                st.success("წარმატებით დაემატა!")
                st.rerun()
            else:
                st.warning("გ
