import streamlit as st
import pandas as pd
import os
from datetime import date

# --------------------
# 【初期設定】
# --------------------
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'health' not in st.session_state:
    st.session_state.health = 0
if 'mental' not in st.session_state:
    st.session_state.mental = 0
if 'strength' not in st.session_state:
    st.session_state.strength = 0
if 'cool' not in st.session_state:
    st.session_state.cool = 0

# --------------------
# 【日付 & CSV設定】
# --------------------
today = str(date.today())
csv_path = "record.csv"

if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=[
        "日付", "日別日", "日常の選択", "日別約", "日別金", "健康", "精神", "筋力", "かっこよさ"
    ])
    df_init.to_csv(csv_path, index=False)

# --------------------
# 【スタイル設定】
# --------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #000000;
    color: white;
}
div[data-testid="stHorizontalBlock"] > div {
    background-color: #111111;
    color: white;
    border-radius: 8px;
    padding: 8px;
}
input, textarea {
    background-color: #222222;
    color: white;
    border: 1px solid #555;
}
button {
    background-color: #333333;
    color: white;
    border: 1px solid #888;
}
.stButton > button {
    color: white !important;
    background-color: #333333;
    border: 1px solid #888;
}
label, .stTextInput > label, .stNumberInput > label {
    color: white !important;
}
.css-1cpxqw2 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# 【レベル計算関数】
# --------------------
def get_level(days):
    if days <= 100:
        return int(days * 0.5)
    elif days <= 1095:
        return int(50 + ((days - 100) / (1095 - 100)) ** 0.7 * 49)
    else:
        return 99

def get_level_progress(days):
    level = get_level(days)
    for i in range(1, 100):
        if get_level(i) >= level:
            current_level_start = i
            break
    for i in range(current_level_start + 1, 1100):
        if get_level(i) > level:
            next_level_start = i
            break
    progress = (days - current_level_start) / (next_level_start - current_level_start)
    return level, progress

# --------------------
# 【タイトル】
# --------------------
st.title("🎮 断酒クエスト")

# --------------------
# 【日別選択】
# --------------------
st.markdown("## 🍺 今日の断酒状況")
drink_choice = st.radio(
    "今日はどっち？",
    ("-- 選択 --", "酒の誘惑に打ち勝った", "仕事などで飲めなかった")
)

did_abstain = False
if drink_choice == "酒の誘惑に打ち勝った":
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    st.session_state.cool += 1
    did_abstain = True
    st.success("酒の誘惑モンスターを倒した！ +1500G 健康+1 精神+1 かっこよさ+1")
elif drink_choice == "仕事などで飲めなかった":
    st.session_state.health += 1
    st.session_state.mental += 1
    st.info("酒は飲めなかったけど、健康+1 精神+1")

# --------------------
# 【食費】
# --------------------
saved_money = 0
expense = st.number_input("📜 今日の食費は？ (円)", min_value=0, step=1)
if st.button("💰 節穫を計算"):
    savings = 1500 - expense
    if savings > 0:
        st.session_state.gold += savings
        st.session_state.health += 1
        saved_money = savings
        st.success(f"{savings} 円節穫！ +{savings}G 健康+1")
    else:
        st.info("今日は節穫できなかったみたい...")

# --------------------
# 【運動】
# --------------------
did_exercise = False
if st.button("🏋️ 運動した"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    did_exercise = True
    st.success("運動成功！ 筋力+1 かっこよさ+1")

# --------------------
# 【セーブ】
# --------------------
if st.button("📅 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "日別日": date.today().strftime("%A"),
            "日常の選択": drink_choice,
            "日別約": saved_money,
            "日別金": st.session_state.gold,
            "健康": st.session_state.health,
            "精神": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！")
    else:
        st.warning("今日はすでにセーブされています")

# --------------------
# 【経験値レベル表示】
# --------------------
df_all = pd.read_csv(csv_path)
continuation_days = len(df_all)
level, progress = get_level_progress(continuation_days)

st.markdown(f"### 🏋️ レベル: {level}  (続けて{continuation_days}日)")
st.progress(progress)

# --------------------
# 【ステータス表示】
# --------------------
st.markdown("## 🧙‍♂️ ステータス")
st.markdown("""
<style>
.stat-table {
    border: 3px double #888888;
    background-color: #111111;
    color: white;
    padding: 10px;
    font-size: 18px;
    font-family: 'M PLUS Rounded 1c', sans-serif;
    width: fit-content;
}
.stat-table .row {
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}
.stat-table .row span:first-child {
    margin-right: 20px;
}
.stat-table .row span:last-child {
    text-align: right;
    min-width: 50px;
    display: inline-block;
}
</style>
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{gold} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span> {health}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span> {mental}</span></div>
  <div class="row"><span>💪 こうげき力</span><span> {strength}</span></div>
  <div class="row"><span>😎 かっこよさ</span><span> {cool}</span></div>
</div>
""".format(
    gold=st.session_state.gold,
    health=st.session_state.health,
    mental=st.session_state.mental,
    strength=st.session_state.strength,
    cool=st.session_state.cool
), unsafe_allow_html=True)

# --------------------
# 【記録一覧へのボタン】
# --------------------
if st.button("📓 記録一覧をみる"):
    st.session_state.page = "record"

# --------------------
# 【記録表示、または戻る】
# --------------------
if st.session_state.get("page") == "record":
    st.title("📓 記録一覧")
    df = pd.read_csv(csv_path)
    st.dataframe(df)
    if st.button("⬅ ホームへ戻る"):
        st.session_state.page = "home"
