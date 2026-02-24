import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Sport Match Maker", layout="wide")

# Инициализация базы данных в памяти (сессии)
# Используем сессию, чтобы данные жили, пока открыта вкладка
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ Организация спортивных встреч")

# Создаем вкладки
tab1, tab2, tab3 = st.tabs(["Все мероприятия", "➕ Создать игру", "📩 Запросы"])

# --- ТАБ 2: СОЗДАНИЕ (Сначала логика создания) ---
with tab2:
    st.header("Новое мероприятие")
    with st.form("create_form", clear_on_submit=True):
        sport = st.selectbox("Вид спорта", ["Футбол", "Баскетбол", "Теннис", "Волейбол", "Другое"])
        place = st.text_input("Место проведения (адрес)")
        date = st.date_input("Дата", datetime.now())
        time = st.time_input("Время")
        max_p = st.number_input("Сколько человек нужно?", min_value=2, max_value=50, value=10)
        
        submitted = st.form_submit_button("Опубликовать")
        if submitted and place:
            new_event = {
                'sport': sport,
                'place': place,
                'date': str(date),
                'time': str(time),
                'max_people': max_p,
                'confirmed': 1, 
                'creator': "Admin" 
            }
            st.session_state.events.append(new_event)
            st.success("Игра создана! Перейдите во вкладку 'Все мероприятия'.")
            st.rerun() # ПЕРЕЗАГРУЗКА, чтобы данные появились везде

# --- ТАБ 1: СПИСОК МЕРОПРИЯТИЙ ---
with tab1:
    st.header("Список доступных игр")
    if not st.session_state.events:
        st.info("Пока нет активных игр. Создайте первую игру во вкладке 'Создать игру'!")
    else:
        # Показываем игры в обратном порядке (новые сверху)
        for idx, event in enumerate(reversed(st.session_state.events)):
            # Вычисляем реальный индекс, так как мы развернули список
            real_idx = len(st.session_state.events) - 1 - idx
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{event['sport']} — {event['place']}")
                    st.write(f"📅 **Дата:** {event['date']} | ⏰ **Время:** {event['time']}")
                    st.write(f"👥 **Участники:** {event['confirmed']}/{event['max_people']}")
                with col2:
                    if event['confirmed'] < event['max_people']:
                        if st.button(f"Записаться", key=f"join_{real_idx}"):
                            st.session_state.requests.append({
                                'event_id': real_idx,
                                'user': f"Player_{random.randint(100, 999)}", 
                                'status': 'pending'
                            })
                            st.toast("Запрос отправлен!")
                    else:
                        st.error("Мест нет")

# --- ТАБ 3: ЗАПРОСЫ ---
with tab3:
    st.header("Управление участниками")
    pending_reqs = [r for r in st.session_state.requests if r['status'] == 'pending']
    
    if not pending_reqs:
        st.write("Новых запросов нет.")
    
    for r_idx, req in enumerate(st.session_state.requests):
        if req['status'] == 'pending':
            ev = st.session_state.events[req['event_id']]
            with st.expander(f"Запрос от {req['user']} на {ev['sport']}"):
                c1, c2 = st.columns(2)
                if c1.button("✅ Принять", key=f"ok_{r_idx}"):
                    st.session_state.events[req['event_id']]['confirmed'] += 1
                    req['status'] = 'accepted'
                    st.rerun()
                if c2.button("❌ Отклонить", key=f"no_{r_idx}"):
                    req['status'] = 'rejected'
                    st.rerun()
