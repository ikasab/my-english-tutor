import streamlit as st
import pandas as pd
from datetime import datetime
import random
import requests
from streamlit_searchbox import st_searchbox

# Настройка страницы
st.set_page_config(page_title="Sport App", page_icon="⚽")

# Инициализация хранилища
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

# Функция поиска адреса
def search_address(search_term: str):
    if not search_term or len(search_term) < 3:
        return []
    url = f"https://photon.komoot.io/api/?q={search_term}&limit=5&lat=41.71&lon=44.82"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            features = response.json().get("features", [])
            results = []
            for f in features:
                p = f.get("properties", {})
                name = p.get("name", "")
                city = p.get("city", "")
                label = f"{name} {city}".strip()
                coords = f.get("geometry", {}).get("coordinates", [0, 0])
                results.append((label, {"label": label, "lat": coords[1], "lon": coords[0]}))
            return results
    except:
        return []
    return []

st.title("⚽ სპორტული პლატფორმა")

tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- TAB 1: LIST ---
with tab1:
    if not st.session_state.events:
        st.info("თამაშები არ არის")
    else:
        for idx, ev in enumerate(reversed(st.session_state.events)):
            r_idx = len(st.session_state.events) - 1 - idx
            with st.container(border=True):
                st.subheader(f"{ev['sport']} - {ev['place']}")
                st.write(f"📅 {ev['date']} | ⏰ {ev['time']}")
                st.write(f"👥 {ev['confirmed']}/{ev['max_p']}")
                if ev['lat'] and ev['lon']:
                    st.map(pd.DataFrame({'lat':[ev['lat']], 'lon':[ev['lon']]}), zoom=14)
                if ev['confirmed'] < ev['max_p']:
                    if st.button("ჩაწერა", key=f"j_{r_idx}", use_container_width=True):
                        st.session_state.requests.append({'ev_id': r_idx, 'user': f"Gamer{random.randint(1,99)}", 'status': 'pending'})
                        st.toast("გაიგზავნა")

# --- TAB 2: CREATE ---
with tab2:
    st.subheader("ახალი თამაში")
    addr = st_searchbox(search_address, key="addr_search", label="მისამართი")
    sport = st.selectbox("სახეობა", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
    col1, col2 = st.columns(2)
    d_v = col1.date_input("თარიღი")
    t_v = col2.time_input("დრო")
    m_p = st.slider("ხალხი", 2, 22, 10)
    
    if st.button("გამოქვეყნება 🚀", use_container_width=True):
        if addr:
            st.session_state.events.append({
                'sport': sport, 'place': addr['label'], 'date': str(d_v),
                'time': str(t_v), 'max_p': m_p, 'confirmed': 1,
                'lat': addr['lat'], 'lon': addr['lon']
            })
            st.success("წარმატებით დაემატა")
            st.rerun()
        else:
            st.error("აირჩიეთ მისამართი")

# --- TAB 3: REQUESTS ---
with tab3:
    st.subheader("მოთხოვნები")
    pending = [r for r in st.session_state.requests if r['status'] == 'pending']
    if not pending:
        st.write("სიახლეები არ არის")
    else:
        for r_i, r in enumerate(st.session_state.requests):
            if r['status'] == 'pending':
                e = st.session_state.events[r['ev_id']]
                with st.expander(f"{r['user']} - {e['sport']}"):
                    c1, c2 = st.columns(2)
                    if c1.button("✅", key=f"a_{r_i}"):
                        st.session_state.events[r['ev_id']]['confirmed'] += 1
                        r['status'] = 'accepted'
                        st.rerun()
                    if c2.button("❌", key=f"r_{r_i}"):
                        r['status'] = 'rejected'
                        st.rerun()
