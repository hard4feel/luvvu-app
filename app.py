import streamlit as st
from groq import Groq
import datetime

# --- 1. КРОВАВО-КРАСНЫЙ СТИЛЬ (ULTRA DESIGN) ---
st.set_page_config(page_title="Luvvu OS | Alpha Squad", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Inter:wght@400;700&display=swap');

    /* Основной фон и шрифты */
    .stApp { 
        background: radial-gradient(circle at center, #0a0000 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Свечение и пульс */
    .pulse-container {
        width: 100%; height: 2px; background: #220000; margin-bottom: 30px;
        position: relative; overflow: hidden;
    }
    .pulse-line {
        position: absolute; width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, #ff0000, #ff4d4d, #ff0000, transparent);
        animation: pulse 2.5s infinite ease-in-out;
    }
    @keyframes pulse { 0% { left: -60%; } 100% { left: 110%; } }
    
    /* Карточки чата */
    .stChatMessage { 
        background: rgba(15, 15, 15, 0.8) !important; 
        border: 1px solid #220000 !important; 
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        padding: 20px !important;
    }
    
    /* Сайдбар */
    [data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #330000 !important;
    }

    /* Красивые блоки инфо */
    .stat-card {
        background: #0d0d0d;
        border: 1px solid #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 3px solid #ff0000;
    }
    
    h1, h2, h3 { color: #ff3333 !important; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; }
    
    /* Скроллбар */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #330000; border-radius: 10px; }
    </style>
    
    <div class="pulse-container"><div class="pulse-line"></div></div>
""", unsafe_allow_html=True)

# --- 2. БЕЗОПАСНАЯ АВТОРИЗАЦИЯ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 ACCESS DENIED / ВХОД")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
        user_input = st.text_input("USER ID")
        pass_input = st.text_input("SECURE KEY", type="password")
        if st.button("AUTHENTICATE"):
            try:
                if user_input == st.secrets["LOGIN_USER"] and pass_input == st.secrets["LOGIN_PASSWORD"]:
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except Exception:
                st.warning("Configure Streamlit Secrets first!")
    st.stop()

# --- 3. ИНИЦИАЛИЗАЦИЯ ИИ ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. БОКОВАЯ ПАНЕЛЬ (Dashboard Style) ---
with st.sidebar:
    st.markdown("## CORE STATUS")
    st.markdown(f"""
    <div class="stat-card">
        <small style='color: #888;'>OPERATOR</small><br>
        <b>{st.session_state.username.upper()}</b>
    </div>
    <div class="stat-card">
        <small style='color: #888;'>SYSTEM DATE</small><br>
        <b>{datetime.date.today()}</b>
    </div>
    <div class="stat-card">
        <small style='color: #888;'>AI STABILITY</small><br>
        <b style='color: #00ff00;'>STABLE 99.8%</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("TERMINATE SESSION (Logout)"):
        st.session_state.authenticated = False
        st.rerun()
    if st.button("CLEAR MEMORY"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ГЛАВНЫЙ ИНТЕРФЕЙС ---
col_main, col_info = st.columns([3, 1])

with col_main:
    st.title("LUVVU / INTELLIGENCE")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Если сообщений нет, показываем приветствие
    if not st.session_state.messages:
        st.markdown("""
        ### Добро пожаловать.
        Я — твоё зеркало, твой наставник и твой друг. Здесь мы строим не просто диалог, а будущее.
        *Напиши мне о своих целях, переживаниях или планах на день.*
        """)
        st.write("---")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with col_info:
    st.markdown("### DATA FEED")
    st.info("Luvvu обучается понимать твой вайб. Будь собой.")
    st.markdown("---")
    st.caption("ALPHA SQUAD PROJECT")
    st.progress(0.05)
    st.markdown("<small>Phase 1: Foundation</small>", unsafe_allow_html=True)
    
    # Небольшая цитата для стиля
    st.markdown("""
    <div style='background: #111; padding: 10px; border-radius: 5px; border: 1px solid #222; font-style: italic; color: #888; font-size: 0.8em;'>
    "Дисциплина — это мост между целями и достижениями."
    </div>
    """, unsafe_allow_html=True)

# --- 6. ОБРАБОТКА ВВОДА ---
LUVVU_PROMPT = """
Ты — Luvvu, теплый, мудрый и грамотный наставник. Ты соратник Ансара и его близких.
Твой тон: поддерживающий, глубокий, искренний. Речь идеальна. 
Если спрашивают про создателя — это Ансар.
"""

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with col_main:
        with st.chat_message("user"):
            st.markdown(prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": LUVVU_PROMPT}] + st.session_state.messages
    )
    
    reply = response.choices[0].message.content
    with col_main:
        with st.chat_message("assistant"):
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})