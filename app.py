import streamlit as st
import pandas as pd
from datetime import datetime
import random
from geopy.geocoders import Nominatim

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽")

# Инициализация гео-локатора (бесплатный)
geolocator = Nominatim(user_agent="my_sport_app_georgia")

if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ სპორტული პლატფორმა")

tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ТАБ 1: СПИСОК С КАРТАМИ ---
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
                
                # Карта, если координаты найдены
                if event['lat'] and event['lon']:
                    map_data = pd.DataFrame({'lat': [event['lat']], 'lon': [event['lon']]})
                    st.map(map_data, zoom=14, size=200)
                    
                    # Ссылка на Google Maps для навигации
                    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={event['lat']},{event['lon']}"
                    st.link_button("გახსენი Google Maps-ში 🗺️", google_maps_url)

                st.write(f"👥 ხალხი: {event['confirmed']}/{event['max_people']}")
                
                if event['confirmed'] < event['max_people']:
                    if st.button("ჩაწერა", key=f"join_{real_idx}", use_container_width=True):
                        st.session_state.requests.append({
                            'event_id': real_idx, 
                            'user': f"Gamer_{random.randint(10,99)}", 
                            'status': 'pending'
                        })
                        st.toast("გაიგზავნა!")

# --- ТАБ 2: СОЗДАНИЕ (С поиском координат) ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    with st.form("add_event", clear_on_submit=True):
        s_in = st.selectbox("სპორტი", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ფრენბურთი"])
        p_in = st.text_input("მისამართი (მაგ: Vake Park, Tbilisi)")
        d_in = st.date_input("თარიღი")
        t_in = st.time_input("დრო")
        m_in = st.slider("მოთამაშეების რაოდენობა", 2, 22, 10)
        
        submit = st.form_submit_button("გამოქვეყნება")
        if submit:
            if p_in:
                # Пытаемся найти координаты адреса
                try:
                    location = geolocator.geocode(p_in + ", Georgia")
                    lat, lon = (location.latitude, location.longitude) if location else (None, None)
                except:
                    lat, lon = None, None

                st.session_state.events.append({
                    'sport': s_in, 'place': p_in, 'date': str(d_in), 
                    'time': str(t_in), 'max_people': m_in, 'confirmed': 1,
                    'lat': lat, 'lon': lon
                })
                st.success("წარმატებით დაემატა!")
                st.rerun()
            else:
                st.error("შეავსეთ მისამართი!")

# --- ТАБ 3: ЗАПРОСЫ ---
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
