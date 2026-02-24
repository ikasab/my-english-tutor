import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽", layout="centered")

# Данные (храним в сессии)
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

# Дизайн (CSS)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }
    .event-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ სპორტული პლატფორმა")

# СОЗДАЕМ ВКЛАДКИ
tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ВКЛАДКА 1: СПИСОК ---
with tab1:
    st.subheader("აქტიური თამაშები")
    if not st.session_state.events:
        st.write("თამაშები არ არის 🤷‍♂️")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            st.markdown(f"""
                <div class="event-card">
                    <h4>{event['sport']} — {event['place']}</h4>
                    <p>📅 {event['date']} | ⏰ {event['time']}</p>
                    <p>👥 {event['confirmed']}/{event['max_people']}</p>
                </div>
            """, unsafe_allow_html=True)
            if event['confirmed'] < event['max_people']:
                if st.button(f"ჩაწერა #{real_idx}", key=f"j_{real_idx}"):
                    st.session_state.requests.append({'event_id': real_idx, 'user': f"Gamer_{random.randint(1,99)}", 'status': 'pending'})
                    st.toast("გაიგზავნა!")

# --- ВКЛАДКА 2: СОЗДАНИЕ (Проверь тут!) ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    # Используем контейнер, чтобы форма была четко видна
    with st.container(border=True):
        sport_in = st.selectbox("სპორტი", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
        place_in = st.text_input("მისამართი", placeholder="მაგ: დიღმის მასივი, იმედის სტადიონი")
        col1, col2 = st.columns(2)
        date_in = col1.date_input("თარიღი")
        time_in = col2.time_input("დრო")
        max_p_in = st.slider("მოთამაშეები", 2, 22, 10)
        
        btn = st.button("გამოქვეყნება 🚀", use_container_width=True)
        
        if btn:
            if place_in:
                st.session_state.events.append({
                    'sport': sport_in, 'place': place_in, 
                    'date': str(date_in), 'time': str(time_in), 
                    'max_people': max_p_in, 'confirmed': 1
                })
                st.success("წარმატებით დაემატა!")
                st.balloons()
                # После успеха перекидываем пользователя на первую вкладку (через rerun)
                st.rerun()
            else:
                st.error("გთხოვთ მიუთითოთ მისამართი!")

# --- ВКЛАДКА 3: ЗАПРОСЫ ---
with tab3:
    st.subheader("მოსული მოთხოვნები")
    has_pending = False
    for r_idx, r in enumerate(st.session_state.requests):
        if r['status'] == 'pending':
            has_pending = True
            ev = st.session_state.events[r['event
