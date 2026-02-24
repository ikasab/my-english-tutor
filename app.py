import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
from textblob import TextBlob
import io
import random

st.set_page_config(page_title="English Tutor NoKey", page_icon="🎓")

# Список вопросов для общения
if 'question' not in st.session_state:
    st.session_state.question = "What is your favorite hobby and why?"

questions = [
    "What is your favorite hobby and why?",
    "Tell me about your best friend.",
    "What did you eat for breakfast today?",
    "Where would you like to travel in the future?",
    "What is your favorite movie?",
    "Do you prefer coffee or tea?"
]

st.title("🎓 English Conversation Coach")
st.write("---")
st.subheader("Question for you:")
st.warning(st.session_state.question)

# Кнопка для смены вопроса
if st.button("Next Question ➡️"):
    st.session_state.question = random.choice(questions)
    st.rerun()

# Запись голоса
text = speech_to_text(start_prompt="Answer by voice 🎙️", stop_prompt="Stop 🛑", language='en-US')

if text:
    st.markdown(f"**You said:** {text}")
    
    # Исправление ошибок через TextBlob
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    
    if corrected_text.lower() != text.lower():
        st.subheader("Correction:")
        st.success(f"It's better to say: {corrected_text}")
        response = f"I corrected you a bit. You should say: {corrected_text}. Good try! Let's continue."
    else:
        st.subheader("Perfect!")
        st.balloons()
        response = f"Great! Your English is perfect. You said: {text}."

    # Озвучка ответа
    tts = gTTS(text=response, lang='en')
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    st.audio(audio_io, format='audio/mp3', autoplay=True)

st.write("---")
st.caption("Эта версия работает без API ключей, используя локальную библиотеку исправления текста.")
