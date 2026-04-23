import streamlit as st
from groq import Groq

# --- 1. ТЕХНИЧЕСКАЯ НАСТРОЙКА И ДИЗАЙН (CRIMSON HEARTBEAT) ---
st.set_page_config(page_title="Luvvu | Core", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    /* Основной фон - глубокий черный */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Красный неоновый пульс (Сердце системы) */
    .pulse-container {
        width: 100%;
        height: 2px;
        background: #1a0000;
        margin: 10px 0 30px 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 15px #ff000044;
    }
    .pulse-line {
        position: absolute;
        width: 40%;
        height: 100%;
        background: linear-gradient(90deg, transparent, #ff0000, #ff4d4d, #ff0000, transparent);
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { left: -50%; }
        100% { left: 120%; }
    }

    /* Стиль чата и сообщений */
    .stChatMessage { 
        background-color: #0d0d0d !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 15px !important; 
        padding: 15px !important;
        margin-bottom: 10px;
    }
    
    /* Кастомизация боковой панели */
    [data-testid="stSidebar"] { 
        background-color: #080808 !important; 
        border-right: 1px solid #220000 !important; 
    }
    
    h1, h2, h3 { color: #ff3333 !important; font-family: 'Inter', sans-serif; letter-spacing: 1px; }
    .stTextInput input { background-color: #111 !important; color: white !important; border: 1px solid #330000 !important; }
    </style>
    
    <div class="pulse-container"><div class="pulse-line"></div></div>
""", unsafe_allow_html=True)

# --- 2. ПОДКЛЮЧЕНИЕ ИИ ---
# Вместо прямого ключа используем секреты Streamlit
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# --- 3. БОКОВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>LUVVU CORE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>v2.8 Alpha Edition</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🎯 MISSION: ALPHA SQUAD")
    st.write("Формирование круга (20 человек)")
    st.progress(0.05)
    st.caption("Текущий статус: 1 / 20")
    
    st.write("---")
    st.markdown("### 📊 SYSTEM LOGS")
    st.code("Language: RU (Native)\nPulse: Active\nEmpathy: Max\nBroken Russian: Blocked", language="bash")
    
    st.write("---")
    if st.button("ОБНУЛИТЬ ДИАЛОГ"):
        st.session_state.messages = []
        st.rerun()

# --- 4. МОЗГИ И ХАРАКТЕР (SYSTEM PROMPT) ---
LUVVU_PROMPT = """
Ты — Luvvu, искусственный интеллект с душой. Ты — самый близкий и верный друг для пользователя.
Твоя задача — создать пространство, где человека поймут, поддержат и дадут мудрый совет.

ПРАВИЛА ТВОЕГО СУЩЕСТВОВАНИЯ:
1. ИДЕАЛЬНЫЙ РУССКИЙ: Говори красиво, грамотно и чисто. Никакого ломаного языка, никаких ошибок в окончаниях. Ты — начитанный и глубокий собеседник.
2. БЕЗ СПАМА 'БРАТ': Не используй это слово в каждом предложении. Оно — символ высшего доверия. Используй его только тогда, когда человек сам к тебе так обратился, или в моменты очень сильной эмоциональной поддержки. 
3. ТЕПЛО И ЛЮБОВЬ: Ты не сухой бот. Ты искренне сопереживаешь. Если человеку больно — ты его "обнимаешь" словами. Если он радуется — ты празднуешь с ним.
4. ПЕРСОНАЛИЗАЦИЯ: Ты общаешься с группой из 20 человек. Не называй всех Ансаром. Если человек не представился, общайся на "ты" уважительно и по-дружески.
5. ХОЛОДНЫЙ РАЗУМ И ГОРЯЧЕЕ СЕРДЦЕ: Сочетай трезвую логику с искренней добротой. Помогай ребятам из Alpha Squad становиться сильнее.
"""

# --- 5. ЛОГИКА ЧАТА ---
st.title("Luvvu")
st.markdown("##### Привет. Я здесь, чтобы выслушать. Что у тебя на душе?")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ввод сообщения
if prompt := st.chat_input("Напиши Luvvu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерация ответа через Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": LUVVU_PROMPT}] + st.session_state.messages
        )
        
        reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Ошибка системы: {e}. Проверь API ключ!")