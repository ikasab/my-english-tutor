import streamlit as st
import pandas as pd
from datetime import datetime
import random
import requests
from streamlit_searchbox import st_searchbox

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽")

# Функция для поиска подсказок адреса (Autocomplete)
def search_address(search_term: str):
    if not search_term or len(search_term) < 3:
        return []
    
    # Используем бесплатный API Photon (OpenStreetMap)
    # Он хорошо ищет на грузинском и английском
    url = f"https://photon.komoot.io/api/?q={search_term}&limit=5&lat=41.7151&lon=44.8271"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            
            results = []
            for f in features:
                p = f.get("properties", {})
                # Собираем красивое название из доступных полей
                name = p.get("name", "")
                city = p.get("city", "")
                street = p.get("street", "")
                
                full_label = f"{name} {street} {city}".strip()
                # Сохраняем и название, и координаты в объекте
                coords = f.get("geometry", {}).get("coordinates", [None, None])
                results.append((full_label, {"label": full_label, "lat": coords[1], "lon": coords[0]}))
            return results
    except:
        return []
    return []

if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

st.title("⚽ სპორტული პლატფორმა")

tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- TAB 1: LIST ---
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
                
                if event.get('lat') and event.get('lon'):
                    map_df = pd.DataFrame({'lat': [event['lat']], 'lon': [event['lon']]})
                    st.map(map_df, zoom=14)

                if st.button("ჩაწერა", key=f"join_{real_idx}", use_container_width=True):
                    st.session_state.requests.append({
                        'event_id': real_idx, 'user': f"მოთამაშე_{random.randint(10,99)}", 'status': 'pending'
                    })
                    st.toast("გაიგზავნა!")

# --- TAB 2: CREATE WITH AUTOCOMPLETE ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    
    # ВАЖНО: Вкладка "Создать" теперь содержит живой поиск
    selected_address = st_searchbox(
        search_address,
        key="address_search",
        label="ჩაწერეთ მისამართი (მისამართის ძიება...)",
        placeholder="მაგ: Vake Park ან ვაკის პარკი"
    )

    with st.form("add_event_form", clear_on_submit=True):
        s_in = st.selectbox("სპორტი", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
        d_in = st.date_input("თარიღი")
        t_in = st.time_input("დრო")
        m_in = st.slider("ხალხი", 2, 22, 10)
        
        submit = st.form_submit_button("გამოქვეყნება")
        
        if submit:
            if selected_address:
                st.session_state.events.append({
                    'sport': s_in,
                    'place': selected_address["label"],
                    'date': str(d_in),
                    'time': str(t_in),
                    'max_people': m_in,
                    'confirmed': 1,
                    'lat': selected_address["lat"],
                    'lon': selected_address["lon"]
                })
                st.success("წარმატებით დაემატა!")
                st.rerun()
            else:
                st.warning("გთხოვთ აირჩიოთ მისამართი სიიდან!")
