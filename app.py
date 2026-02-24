import streamlit as st
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai
from gtts import gTTS
import io

# Настройка
st.set_page_config(page_title="English Tutor", page_icon="🇬🇧")
genai.configure(api_key="AIzaSyC5C7rLSOcZ8LqiKmEJcKJcN2lCjBbN9KA") # <-- ПРОВЕРЬ КЛЮЧ ЗДЕСЬ
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🇬🇧 AI English Speaking Club")

# Кнопка записи
text = speech_to_text(start_prompt="Нажми и говори (English) 🎤", stop_prompt="Остановить 🛑", language='en-US')

if text:
    st.info(f"Вы сказали: {text}")
    
    # Запрос к AI
    prompt = f"Act as an English teacher. 1. Correct any mistakes in this sentence: '{text}'. 2. Give a short natural reply to keep the conversation going."
    
    try:
        response = model.generate_content(prompt)
        ai_answer = response.text
        
        # Показываем ответ
        st.subheader("AI Учитель:")
        st.success(ai_answer)
        
        # Озвучка (превращаем текст в звук)
        tts = gTTS(text=ai_answer, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format='audio/mp3', autoplay=True) # Autoplay сразу проиграет звук
        
    except Exception as e:
        st.error(f"Ошибка API: {e}")
        st.warning("Попробуй создать новый API Key в Google AI Studio и заменить его.")
