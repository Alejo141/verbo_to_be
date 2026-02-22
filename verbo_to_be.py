import streamlit as st
import random

st.set_page_config(
    page_title="Verbo To Be Adventure",
    page_icon="👑",
    layout="wide"
)

TOTAL_LIVES = 3
QUESTIONS_PER_LEVEL = 6
MAX_LEVEL = 5

# ---------------- INIT ----------------
if "started" not in st.session_state:
    st.session_state.started = False

# ================= PORTADA =================
if not st.session_state.started:

    st.markdown("""
    <style>
    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
    }

    .title {
        font-size:70px;
        text-align:center;
        color:white;
    }

    .subtitle {
        font-size:32px;
        text-align:center;
        color:white;
        margin-bottom:40px;
    }

    .stButton>button {
        font-size:28px;
        height:90px;
        border-radius:25px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>👑✨ Verbo To Be Adventure ✨👑</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Choose your magical destiny 🌈</div>", unsafe_allow_html=True)

    name = st.text_input("✨ Enter Your Name ✨")

    col1, col2 = st.columns(2)

    with col1:
        princess = st.button("👸🌸 Princess Adventure ✨")

    with col2:
        king = st.button("🤴⚔️ King Adventure 🔥")

    if (princess or king) and name.strip() == "":
        st.warning("✨ Please enter your name ✨")

    if princess and name.strip():
        theme = "princess"
    elif king and name.strip():
        theme = "king"
    else:
        st.stop()

    st.session_state.game = {
        "name": name,
        "theme": theme,
        "level": 1,
        "coins": 0,
        "stars": 0,
        "lives": TOTAL_LIVES
    }

    st.session_state.started = True
    st.rerun()

# ================= GAME =================
game = st.session_state.game

# Emojis por modo
if game["theme"] == "princess":
    header_emoji = "👸🌸✨"
    success_msg = "🎀✨ Amazing Princess! Correct! ✨🎀"
    fail_msg = "💔 Oh no princess! Try again! 💔"
    medal_title = "👑✨ Royal Princess Champion ✨👑"
else:
    header_emoji = "🤴⚔️🔥"
    success_msg = "⚔️🔥 Brave King! Correct! 🔥⚔️"
    fail_msg = "💥 Oh no warrior! Try again! 💥"
    medal_title = "🏆🔥 Supreme King Champion 🔥🏆"

st.markdown("""
<style>
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.stApp {
    background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #84fab0, #8fd3f4);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
}

.title2 {
    font-size:55px;
    text-align:center;
    color:#222;
}

.panel {
    background:white;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:28px;
    margin-bottom:20px;
    color:#222;
}

.question-card {
    background:#ffffff;
    padding:40px;
    border-radius:25px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
    font-size:40px;
    text-align:center;
    color:#222;
    margin-top:20px;
}

.stButton>button {
    font-size:30px;
    height:90px;
    border-radius:30px;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='title2'>{header_emoji} Level {game['level']} {header_emoji}</div>", unsafe_allow_html=True)

st.markdown(
    f"<div class='panel'>✨ {game['name']} ✨ | 🪙 {game['coins']} | ⭐ {game['stars']} | ❤️ {game['lives']}</div>",
    unsafe_allow_html=True
)

# Botón regresar
if st.button("🏠 Back to Home"):
    st.session_state.clear()
    st.rerun()

# ---------------- BANCO PROGRESIVO ----------------
question_bank = {
    1: [
        "I ___ happy.",
        "She ___ kind.",
        "He ___ tall.",
        "They ___ strong.",
        "We ___ ready.",
        "It ___ magic."
    ],
    2: [
        "I ___ very happy today.",
        "She ___ very kind to everyone.",
        "He ___ very brave in battle.",
        "They ___ very excited now.",
        "We ___ ready for school.",
        "It ___ very beautiful."
    ],
    3: [
        "I ___ very happy because I am at the castle.",
        "She ___ very kind when she helps her friends.",
        "He ___ very brave when he fights the dragon.",
        "They ___ very excited about the celebration.",
        "We ___ ready for the magical adventure.",
        "It ___ a beautiful day in the kingdom."
    ],
    4: [
        "She ___ the smartest princess in the kingdom.",
        "He ___ the strongest knight in the empire.",
        "They ___ preparing for the most important battle.",
        "We ___ the heroes of this magical story.",
        "It ___ the biggest challenge of the year.",
        "I ___ proud to be part of this mission."
    ],
    5: [
        "I ___ very excited because today is my coronation day.",
        "She ___ always confident when she speaks to the people.",
        "He ___ responsible for protecting the entire kingdom.",
        "They ___ working together to defeat the powerful dragon.",
        "We ___ determined to win this important battle.",
        "It ___ the most difficult adventure we have ever faced."
    ]
}

if "questions" not in st.session_state:
    st.session_state.questions = random.sample(
        question_bank[game["level"]],
        QUESTIONS_PER_LEVEL
    )
    st.session_state.index = 0

questions = st.session_state.questions

if game["lives"] <= 0:
    st.error("💀 Game Over!")
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# ---------------- GAME LOOP ----------------
if st.session_state.index < len(questions):

    question = questions[st.session_state.index]
    st.progress(st.session_state.index / len(questions))

    st.markdown(f"<div class='question-card'>{question}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    for col, option in zip([col1, col2, col3], ["am", "is", "are"]):
        with col:
            if st.button(option):

                correct = (
                    ("I ___" in question and option == "am") or
                    ("She ___" in question and option == "is") or
                    ("He ___" in question and option == "is") or
                    ("It ___" in question and option == "is") or
                    ("They ___" in question and option == "are") or
                    ("We ___" in question and option == "are") or
                    ("You ___" in question and option == "are")
                )

                if correct:
                    st.success(success_msg)
                    st.balloons()
                    game["coins"] += 1
                    game["stars"] += 1
                else:
                    st.error(fail_msg)
                    game["lives"] -= 1

                st.session_state.index += 1
                st.rerun()

else:
    st.balloons()
    st.markdown(f"## 🏆 {medal_title} 🏆")

    total_stars = game["stars"]

    if total_stars >= 25:
        medal = "🥇 GOLD MEDAL"
    elif total_stars >= 18:
        medal = "🥈 SILVER MEDAL"
    else:
        medal = "🥉 BRONZE MEDAL"

    st.markdown(f"# {medal}")
    st.markdown(f"⭐ Total Stars: {total_stars}")

    if st.button("🔄 Play Again"):
        st.session_state.clear()
        st.rerun()