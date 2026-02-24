import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(page_title="სპორტული თამაშების ორგანიზატორი", layout="wide")

# Инициализация данных в сессии
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ სპორტული შეხვედრების ორგანიზება")

# Создаем вкладки на грузинском
tab1, tab2, tab3 = st.tabs(["ყველა ღონისძიება", "➕ თამაშის შექმნა", "📩 მოთხოვნები"])

# --- ტაბი 2: შექმნა (თამაშის დამატება) ---
with tab2:
    st.header("ახალი ღონისძიება")
    with st.form("create_form", clear_on_submit=True):
        sport = st.selectbox("სპორტის სახეობა", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ფრენბურთი", "სხვა"])
        place = st.text_input("ჩატარების ადგილი (მისამართი)")
        date = st.date_input("თარიღი", datetime.now())
        time = st.time_input("დრო")
        max_p = st.number_input("რამდენი ადამიანია საჭირო?", min_value=2, max_value=50, value=10)
        
        submitted = st.form_submit_button("გამოქვეყნება")
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
            st.success("თამაში წარმატებით შეიქმნა! იხილეთ 'ყველა ღონისძიება'-ს ჩანართში.")
            st.rerun()

# --- ტაბი 1: ღონისძიებების სია ---
with tab1:
    st.header("ხელმისაწვდომი თამაშები")
    if not st.session_state.events:
        st.info("აქტიური თამაშები ჯერ არ არის. შექმენით პირველი თამაში!")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{event['sport']} — {event['place']}")
                    st.write(f"📅 **თარიღი:** {event['date']} | ⏰ **დრო:** {event['time']}")
                    st.write(f"👥 **მონაწილეები:** {event['confirmed']}/{event['max_people']}")
                with col2:
                    if event['confirmed'] < event['max_people']:
                        if st.button(f"ჩაწერა", key=f"join_{real_idx}"):
                            st.session_state.requests.append({
                                'event_id': real_idx,
                                'user': f"მოთამაშე_{random.randint(100, 999)}", 
                                'status': 'pending'
                            })
                            st.toast("მოთხოვნა გაიგზავნა!")
                    else:
                        st.error("ადგილები არ არის")

# --- ტაბი 3: მოთხოვნები ---
with tab3:
    st.header("მონაწილეების მართვა")
    pending_reqs = [r for r in st.session_state.requests if r['status'] == 'pending']
    
    if not pending_reqs:
        st.write("ახალი მოთხოვნები არ არის.")
    
    for r_idx, req in enumerate(st.session_state.requests):
        if req['status'] == 'pending':
            ev = st.session_state.events[req['event_id']]
            with st.expander(f"მოთხოვნა {req['user']}-სგან: {ev['sport']}"):
                c1, c2 = st.columns(2)
                if c1.button("✅ მიღება", key=f"ok_{r_idx}"):
                    st.session_state.events[req['event_id']]['confirmed'] += 1
                    req['status'] = 'accepted'
                    st.rerun()
                if c2.button("❌ უარყოფა", key=f"no_{r_idx}"):
                    req['status'] = 'rejected'
                    st.rerun()
