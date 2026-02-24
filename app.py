import streamlit as st
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai
from gtts import gTTS
import io

# Настройка страницы
st.set_page_config(page_title="AI English Coach", page_icon="🎤")

# Настройка нейросети (Gemini)
# Сюда вставляешь свой бесплатный ключ
genai.configure(api_key="AIzaSyC5C7rLSOcZ8LqiKmEJcKJcN2lCjBbN9KA")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎤 Ваш AI-репетитор английского")
st.write("Нажми кнопку ниже, скажи фразу на английском, и я исправлю твои ошибки!")

# Кнопка записи голоса
text = speech_to_text(
    start_prompt="Начать запись 🎙️",
    stop_prompt="Стоп 🛑",
    language='en-US',
    use_container_width=True,
    key='speech'
)

if text:
    st.markdown(f"**Вы сказали:** `{text}`")
    
    # Промпт для обучения
    prompt = f"Act as a friendly English teacher. First, correct any grammar or pronunciation-style mistakes in my sentence: '{text}'. Then, give a brief and natural response to it. Keep it simple for a learner."
    
    with st.spinner('AI думает...'):
        try:
            response = model.generate_content(prompt)
            answer = response.text
            
            st.subheader("Разбор и ответ:")
            st.info(answer)
            
            # Генерация звука (озвучка ответа AI)
            tts = gTTS(text=answer, lang='en')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            st.audio(audio_io, format='audio/mp3')
            
        except Exception as e:

            st.error("Похоже, нужно проверить API ключ или соединение.")
