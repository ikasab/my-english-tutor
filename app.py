import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sport Match Maker", layout="wide")

# Инициализация базы данных в памяти (сессии)
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ Организация спортивных встреч")

tab1, tab2, tab3 = st.tabs(["Все мероприятия", "➕ Создать игру", "📩 Мои запросы"])

# --- TAB 1: СПИСОК МЕРОПРИЯТИЙ ---
with tab1:
    st.header("Доступные игры")
    if not st.session_state.events:
        st.write("Пока игр нет. Будь первым!")
    else:
        for idx, event in enumerate(st.session_state.events):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{event['sport']} - {event['place']}")
                    st.write(f"📅 **Дата:** {event['date']} | ⏰ **Время:** {event['time']}")
                    st.write(f"👥 **Участники:** {event['confirmed']}/{event['max_people']}")
                with col2:
                    if st.button(f"Записаться", key=f"join_{idx}"):
                        st.session_state.requests.append({
                            'event_id': idx,
                            'user': "User_" + str(random.randint(1, 100)), # Имитация юзера
                            'status': 'pending'
                        })
                        st.toast("Запрос отправлен организатору!")

# --- TAB 2: СОЗДАНИЕ МЕРОПРИЯТИЯ ---
with tab2:
    st.header("Новое мероприятие")
    with st.form("create_form"):
        sport = st.selectbox("Вид спорта", ["Футбол", "Баскетбол", "Теннис", "Волейбол", "Другое"])
        place = st.text_input("Место проведения (название поля/адрес)")
        date = st.date_input("Дата", datetime.now())
        time = st.time_input("Время")
        max_p = st.number_input("Сколько всего человек нужно?", min_value=2, max_value=50, value=10)
        
        submitted = st.form_submit_button("Опубликовать")
        if submitted:
            new_event = {
                'sport': sport,
                'place': place,
                'date': str(date),
                'time': str(time),
                'max_people': max_p,
                'confirmed': 1, # Организатор уже в деле
                'creator': "Admin" 
            }
            st.session_state.events.append(new_event)
            st.success("Игра создана!")
            st.rerun()

# --- TAB 3: ПОДТВЕРЖДЕНИЕ ЗАПРОСОВ ---
with tab3:
    st.header("Управление участниками")
    for req_idx, req in enumerate(st.session_state.requests):
        if req['status'] == 'pending':
            event = st.session_state.events[req['event_id']]
            st.write(f"Запрос от **{req['user']}** на игру **{event['sport']}** ({event['place']})")
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Принять", key=f"acc_{req_idx}"):
                if event['confirmed'] < event['max_people']:
                    event['confirmed'] += 1
                    req['status'] = 'accepted'
                    st.rerun()
                else:
                    st.error("Мест больше нет!")
            
            if c2.button("❌ Отклонить", key=f"rej_{req_idx}"):
                req['status'] = 'rejected'
                st.rerun()
