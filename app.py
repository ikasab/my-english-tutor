import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="Sport App", page_icon="⚽")

# Инициализация данных
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ სპორტული პლატფორმა")

# Вкладки
tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ВКЛАДКА 1: СПИСОК ---
with tab1:
    st.subheader("აქტიური თამაშები")
    if not st.session_state.events:
        st.info("თამაშები არ არის")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            with st.container(border=True):
                st.markdown(f"### {event['sport']}")
                st.write(f"📍 ადგილი: {event['place']}")
                st.write(f"📅 {event['date']} | ⏰ {event['time']}")
                st.write(f"👥 ხალხი: {event['confirmed']}/{event['max_people']}")
                
                if event['confirmed'] < event['max_people']:
                    if st.button("ჩაწერა", key=f"join_{real_idx}"):
                        st.session_state.requests.append({
                            'event_id': real_idx, 
                            'user': f"Gamer_{random.randint(10,99)}", 
                            'status': 'pending'
                        })
                        st.toast("გაიგზავნა!")
                else:
                    st.error("ადგილები არ არის")

# --- ВКЛАДКА 2: СОЗДАНИЕ ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    with st.form("add_event", clear_on_submit=True):
        s_in = st.selectbox("სპორტი", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ფრენბურთი"])
        p_in = st.text_input("მისამართი")
        d_in = st.date_input("თარიღი")
        t_in = st.time_input("დრო")
        m_in = st.slider("მოთამაშეების რაოდენობა", 2, 22, 10)
        
        submit = st.form_submit_button("გამოქვეყნება")
        if submit:
            if p_in:
                st.session_state.events.append({
                    'sport': s_in, 
                    'place': p_in, 
                    'date': str(d_in), 
                    'time': str(t_in), 
                    'max_people': m_in, 
                    'confirmed': 1
                })
                st.success("წარმატებით დაემატა!")
                st.rerun()
            else:
                st.error("შეავსეთ მისამართი!")

# --- ВКЛАДКА 3: ЗАПРОСЫ ---
with tab3:
    st.subheader("მოთხოვნები")
    has_any = False
    for r_idx, req in enumerate(st.session_state.requests):
        if req['status'] == 'pending':
            has_any = True
            ev = st.session_state.events[req['event_id']]
            with st.expander(f"{req['user']} - {ev['sport']}"):
                c1, c2 = st.columns(2)
                if c1.button("✅ მიღება", key=f"acc_{r_idx}"):
                    st.session_state.events[req['event_id']]['confirmed'] += 1
                    req['status'] = 'accepted'
                    st.rerun()
                if c2.button("❌ უარყოფა", key=f"rej_{r_idx}"):
                    req['status'] = 'rejected'
                    st.rerun()
    if not has_any:
        st.write("ახალი მოთხოვნები არ არის")
