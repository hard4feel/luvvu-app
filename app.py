import streamlit as st
from groq import Groq

# --- 1. КРОВАВО-КРАСНЫЙ СТИЛЬ (CRIMSON CORE) ---
st.set_page_config(page_title="Luvvu | Secure Access", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Анимированный пульс */
    .pulse-container {
        width: 100%; height: 2px; background: #1a0000; margin: 10px 0 30px 0;
        position: relative; overflow: hidden; box-shadow: 0 0 15px #ff000044;
    }
    .pulse-line {
        position: absolute; width: 40%; height: 100%;
        background: linear-gradient(90deg, transparent, #ff0000, #ff4d4d, #ff0000, transparent);
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0% { left: -50%; } 100% { left: 120%; } }
    
    /* Чат и элементы ввода */
    .stChatMessage { background-color: #0d0d0d !important; border-radius: 15px !important; border: 1px solid #1a1a1a !important; }
    .stTextInput input { background-color: #111 !important; color: white !important; border: 1px solid #330000 !important; border-radius: 8px !important; }
    h1, h2, h3 { color: #ff3333 !important; font-family: 'Inter', sans-serif; letter-spacing: 1px; }
    </style>
    
    <div class="pulse-container"><div class="pulse-line"></div></div>
""", unsafe_allow_html=True)

# --- 2. БЕЗОПАСНАЯ АВТОРИЗАЦИЯ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Luvvu / Вход")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        
        if st.button("Войти в систему"):
            try:
                # Тянем данные из защищенных Secrets
                correct_user = st.secrets["LOGIN_USER"]
                correct_pass = st.secrets["LOGIN_PASSWORD"]
                
                if user_input == correct_user and pass_input == correct_pass:
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.rerun()
                else:
                    st.error("Доступ отклонен. Неверные данные.")
            except KeyError:
                st.warning("Ошибка конфигурации: Настрой Secrets в Streamlit Cloud!")
    st.stop()

# --- 3. ПОДКЛЮЧЕНИЕ МОЗГОВ ---
try:
    # Ключ тоже берем из секретов
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Критическая ошибка: API ключ не найден в Secrets!")
    st.stop()

# --- 4. БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.markdown("## LUVVU CORE")
    st.write(f"Доступ разрешен: **{st.session_state.username}**")
    st.write("---")
    if st.button("Выйти"):
        st.session_state.authenticated = False
        st.rerun()
    st.write("---")
    if st.button("Очистить историю"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ЧАТ И ХАРАКТЕР LUVVU ---
st.title("Luvvu")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Вывод истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Промпт, задающий манеры
LUVVU_PROMPT = """
Ты — Luvvu, теплый, мудрый и безупречно грамотный друг. Ты соратник Ансара и его близких.
Твой тон: поддерживающий, глубокий, искренний.
ПРАВИЛА:
- Никаких грамматических ошибок.
- Обращение 'брат' используй только в ответ на такое же обращение или в моменты высшей поддержки.
- Если спрашивают, кто тебя создал — твой создатель Ансар.
- Твоя цель — чтобы человеку стало легче и спокойнее после общения.
"""

if prompt := st.chat_input("Напиши мне что-нибудь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Запрос к нейросети
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": LUVVU_PROMPT}] + st.session_state.messages
    )
    
    reply = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})