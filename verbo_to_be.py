import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Royal Grammar Adventure", page_icon="👑", layout="wide")

SAVE_FILE = "royal_save.json"
QUESTIONS_PER_LEVEL = 6
TOTAL_LIVES = 3

# ---------------- SAVE SYSTEM ----------------
def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def reset_game():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

# ---------------- LOAD GAME ----------------
if "game" not in st.session_state:
    saved = load_game()
    if saved:
        st.session_state.game = saved
    else:
        st.session_state.game = {
            "name": "",
            "mode": "",
            "world": 1,
            "coins": 0,
            "lives": TOTAL_LIVES
        }

game = st.session_state.game

# ---------------- MODE SELECTION ----------------
if game["mode"] == "":
    st.markdown("## 👑 Choose Your Character 👑")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👸 Princess Mode"):
            game["mode"] = "princess"
            save_game(game)
            st.rerun()

    with col2:
        if st.button("⚔️ Knight Mode"):
            game["mode"] = "knight"
            save_game(game)
            st.rerun()

    st.stop()

# ---------------- STYLE BY MODE ----------------
if game["mode"] == "princess":
    primary = "#ff4da6"
    background = "#fff0f5"
    progress_color = "#ff4da6"
    icon = "👸"
else:
    primary = "#3366cc"
    background = "#e6f0ff"
    progress_color = "#3366cc"
    icon = "⚔️"

st.markdown(f"""
<style>
.big-title {{
    text-align:center;
    font-size:55px;
    color:{primary};
}}

.question {{
    font-size:36px;
    text-align:center;
    margin-top:30px;
}}

.stButton>button {{
    font-size:26px;
    height:80px;
    width:100%;
    border-radius:20px;
    background-color:{primary};
    color:white;
}}

.panel {{
    background:{background};
    padding:20px;
    border-radius:20px;
    font-size:24px;
    text-align:center;
    color:#444444;
    font-weight:600;
}}

div[data-testid="stProgress"] > div > div > div > div {{
    background-color:{progress_color};
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="big-title">{icon} Royal Grammar Adventure {icon}</div>', unsafe_allow_html=True)

# ---------------- NAME ----------------
if game["name"] == "":
    name = st.text_input("✨ Enter Your Name ✨")
    if name:
        game["name"] = name
        save_game(game)
        st.rerun()
    st.stop()

st.markdown(
    f"<div class='panel'>{icon} {game['name']} | 🌎 World {game['world']} | 🪙 {game['coins']} | ❤️ {game['lives']}</div>",
    unsafe_allow_html=True
)

# ---------------- PROGRESSIVE QUESTION BANK ----------------
question_bank = {

    # 🌎 WORLD 1 – Cortas
    1: [
        {"q": "I ___ happy.", "a": "am", "type": "verb"},
        {"q": "She ___ kind.", "a": "is", "type": "verb"},
        {"q": "They ___ ready.", "a": "are", "type": "verb"},
        {"q": "___ am brave.", "a": "I", "type": "pronoun"},
        {"q": "___ is strong.", "a": "He", "type": "pronoun"},
        {"q": "___ are friends.", "a": "We", "type": "pronoun"},
    ],

    # 🌎 WORLD 2 – Medias
    2: [
        {"q": "I ___ very happy today.", "a": "am", "type": "verb"},
        {"q": "She ___ very kind to everyone.", "a": "is", "type": "verb"},
        {"q": "They ___ very excited now.", "a": "are", "type": "verb"},
        {"q": "___ are ready for battle.", "a": "They", "type": "pronoun"},
        {"q": "___ is my best friend.", "a": "She", "type": "pronoun"},
        {"q": "___ am learning magic.", "a": "I", "type": "pronoun"},
    ],

    # 🌎 WORLD 3 – Largas
    3: [
        {"q": "I ___ very happy because I am at the castle.", "a": "am", "type": "verb"},
        {"q": "She ___ very kind when she helps her friends.", "a": "is", "type": "verb"},
        {"q": "They ___ working together to protect the kingdom.", "a": "are", "type": "verb"},
        {"q": "___ are the heroes of this magical story.", "a": "They", "type": "pronoun"},
        {"q": "___ is ready to become queen someday.", "a": "She", "type": "pronoun"},
        {"q": "___ is a powerful magical creature.", "a": "It", "type": "pronoun"},
    ],

    # 🌎 WORLD 4 – Más complejas
    4: [
        {"q": "We ___ preparing for the most important battle of the year.", "a": "are", "type": "verb"},
        {"q": "He ___ responsible for protecting the entire kingdom.", "a": "is", "type": "verb"},
        {"q": "I ___ proud to be part of this royal mission.", "a": "am", "type": "verb"},
        {"q": "___ are determined to defeat the powerful dragon.", "a": "We", "type": "pronoun"},
        {"q": "___ is the bravest knight in the empire.", "a": "He", "type": "pronoun"},
        {"q": "___ are working together to win this battle.", "a": "They", "type": "pronoun"},
    ]
}

options_verbs = ["am", "is", "are"]
options_pronouns = ["I", "He", "She", "It", "We", "They"]

# ---------------- RANDOMIZE ----------------
if "level_questions" not in st.session_state or st.session_state.get("current_world") != game["world"]:
    bank = question_bank[game["world"]]
    st.session_state.level_questions = random.sample(bank, min(QUESTIONS_PER_LEVEL, len(bank)))
    st.session_state.index = 0
    st.session_state.current_world = game["world"]

questions = st.session_state.level_questions

progress = st.session_state.index / len(questions)
st.progress(progress)

# ---------------- GAME LOOP ----------------
if game["lives"] <= 0:
    st.error("💀 Game Over!")
    if st.button("🔄 Restart"):
        reset_game()
        st.session_state.clear()
        st.rerun()
    st.stop()

if st.session_state.index < len(questions):

    q = questions[st.session_state.index]
    st.markdown(f"<div class='question'>{q['q']}</div>", unsafe_allow_html=True)

    options = options_verbs if q["type"] == "verb" else options_pronouns
    cols = st.columns(len(options))

    for col, option in zip(cols, options):
        with col:
            if st.button(option):
                if option == q["a"]:
                    st.success("✨ Correct! +1 Coin")
                    game["coins"] += 1
                else:
                    st.error("❌ Wrong! -1 Life")
                    game["lives"] -= 1

                save_game(game)
                st.session_state.index += 1
                st.rerun()

else:
    st.balloons()
    st.success(f"🏆 World {game['world']} Complete!")

    if st.button("➡️ Next World"):
        game["world"] += 1
        save_game(game)
        del st.session_state.level_questions
        st.rerun()

# ---------------- RESET ----------------
st.divider()
if st.button("❌ Reset Progress"):
    reset_game()
    st.session_state.clear()
    st.rerun()