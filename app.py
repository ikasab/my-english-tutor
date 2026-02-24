import streamlit as st
import pandas as pd
from datetime import datetime
import random
from geopy.geocoders import Nominatim

# Настройка страницы
st.set_page_config(page_title="Sport App", page_icon="⚽")

# Настройка гео-локатора с увеличенным временем ожидания
geolocator = Nominatim(user_agent="geo_sport_app_v2", timeout=10)

if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ სპორტული პლატფორმა")

tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- TAB 1: СПИСОК ---
with tab1:
    st.subheader("აქტიური თამაშები")
    if not st.session_state.events:
        st.info("თამაშები არ არის")
    else:
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            with st.container(border=True):
                st.markdown(f"### {event['sport']}")
                st.write(f"📍 **მისამართი:** {event['place']}")
                st.write(f"📅 {event['date']} | ⏰ {event['time']}")
                
                # Показываем карту, если координаты есть
                if event.get('lat') and event.get('lon'):
                    map_df = pd.DataFrame({'lat': [event['lat']], 'lon': [event['lon']]})
                    st.map(map_df, zoom=14)
                
                # Кнопка прямой ссылки на Google Maps (всегда работает)
                search_query = event['place'].replace(" ", "+")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={search_query}+Georgia"
                st.link_button("ნახე Google Maps-ზე 🗺️", maps_url)

                st.write(f"👥 ხალხი: {event['confirmed']}/{event['max_people']}")
                
                if event['confirmed'] < event['max_people']:
                    if st.button("ჩაწერა", key=f"join_{real_idx}", use_container_width=True):
                        st.session_state.requests.append({
                            'event_id': real_idx, 
                            'user': f"მოთამაშე_{random.randint(10,99)}", 
                            'status': 'pending'
                        })
                        st.toast("მოთხოვნა გაიგზავნა!")

# --- TAB 2: СОЗДАНИЕ ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    with st.form("add_event", clear_on_submit=True):
        s_in = st.selectbox("სპორტი", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
        p_in = st.text_input("მისამართი (მაგ: Vake Park, Tbilisi)")
        d_in = st.date_input("თარიღი")
        t_in = st.time_input("დრო")
        m_in = st.slider("ხალხი", 2, 22, 10)
        
        submit = st.form_submit_button("გამოქვეყნება")
        
        if submit:
            if p_in:
                lat, lon = None, None
                # Визуальный индикатор поиска координат
                with st.spinner('ვ ეძებთ კოორდინატებს...'):
                    try:
                        location = geolocator.geocode(p_in + ", Georgia")
                        if location:
                            lat, lon = location.latitude, location.longitude
                    except:
                        pass # Если сервис координат упал, просто идем дальше без лагов

                st.session_state.events.append({
                    'sport': s_in, 'place': p_in, 'date': str(d_in), 
                    'time': str(t_in), 'max_people': m_in, 'confirmed': 1,
                    'lat': lat, 'lon': lon
                })
                st.success("წარმატებით დაემატა!")
                st.rerun()
            else:
                st.warning("შეავსეთ მისამართი!")

# --- TAB 3: ЗАПРОСЫ ---
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
        st.write("სიახლეები არ არის")
