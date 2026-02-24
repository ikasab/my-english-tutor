import streamlit as st
import pandas as pd
from datetime import datetime
import random
import requests
from streamlit_searchbox import st_searchbox

# Настройка страницы
st.set_page_config(page_title="Sport App Georgia", page_icon="⚽", layout="centered")

# Инициализация хранилища
if 'events' not in st.session_state:
    st.session_state.events = []
if 'requests' not in st.session_state:
    st.session_state.requests = []

# Функция поиска адреса
def search_address(search_term: str):
    if not search_term or len(search_term) < 3:
        return []
    url = f"https://photon.komoot.io/api/?q={search_term}&limit=5&lat=41.7151&lon=44.8271"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            features = response.json().get("features", [])
            results = []
            for f in features:
                p = f.get("properties", {})
                name = p.get("name", "")
                city = p.get("city", "Tbilisi")
                street = p.get("street", "")
                full_label = f"{name} {street}, {city}".strip()
                coords = f.get("geometry", {}).get("coordinates", [None, None])
                results.append((full_label, {"label": full_label, "lat": coords[1], "lon": coords[0]}))
            return results
    except:
        return []
    return []

st.title("⚽ სპორტული პლატფორმა")

# Вкладки
tab1, tab2, tab3 = st.tabs(["🏠 თამაშები", "➕ შექმნა", "📩 მოთხოვნები"])

# --- ТАБ 1: СПИСОК ИГР ---
with tab1:
    st.subheader("აქტიური თამაშები")
    if not st.session_state.events:
        st.info("თამაშები ჯერ არ არის. შექმენი პირველი!")
    else:
        # Показываем список (новые сверху)
        for idx, event in enumerate(reversed(st.session_state.events)):
            real_idx = len(st.session_state.events) - 1 - idx
            with st.container(border=True):
                st.markdown(f"### {event['sport']} — {event['place']}")
                st.write(f"📅 {event['date']} | ⏰ {event['time']}")
                st.write(f"👥 მონაწილეები: {event['confirmed']}/{event['max_people']}")
                
                if event.get('lat') and event.get('lon'):
                    m_df = pd.DataFrame({'lat': [event['lat']], 'lon': [event['lon']]})
                    st.map(m_df, zoom=14)

                if event['confirmed'] < event['max_people']:
                    if st.button("ჩაწერა 📩", key=f"join_{real_idx}", use_container_width=True):
                        st.session_state.requests.append({
                            'event_id': real_idx, 
                            'user': f"მოთამაშე_{random.randint(10,99)}", 
                            'status': 'pending'
                        })
                        st.success("მოთხოვნა გაიგზავნა!")
                else:
                    st.error("ადგილები შევსებულია")

# --- ТАБ 2: СОЗДАНИЕ (БЕЗ ST.FORM ДЛЯ НАДЕЖНОСТИ) ---
with tab2:
    st.subheader("ახალი თამაშის დამატება")
    
    # 1. Поиск адреса (снаружи формы)
    selected_addr = st_searchbox(
        search_address,
        key="addr_search_new",
        label="მოძებნეთ მისამართი (ინგლისურად ან ქართულად)",
    )
    
    # 2. Остальные поля
    sport_type = st.selectbox("სპორტის სახეობა", ["ფეხბურთი", "კალათბურთი", "ჩოგბურთი", "ვოლიბურთი"])
    
    col_d, col_t = st.columns(2)
    d_val = col_d.date_input("თარიღი", datetime.now())
    t_val = col_t.time_input("დრო")
    
    max_p = st.slider("მოთამაშეების რაოდენობა", 2, 22, 10)
    
    # Кнопка создания
    if st.button("თამაშის გამოქვეყნება 🚀", use_container_width=True):
        if selected_addr:
            # Создаем объект игры
            new_game = {
                'sport': sport_type,
                'place': selected_addr["label"],
                'date': str(d_val),
                'time': str(t_val),
                'max_people': max_p,
                'confirmed': 1,
                'lat': selected_addr["lat"],
                'lon': selected_addr["lon"]
            }
            # Добавляем в список
            st.session_state.events.append(new_game)
            st.balloons()
            st.success("თამაში წარმატებით დაემატა!")
            # Пауза и перезагрузка для обновления списка
            st.rerun()
        else:
            st.error("გთ
