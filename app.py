import streamlit as st
import pandas as pd
import os
from datetime import date

# ステータスの初期化
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

# 日付取得
today = str(date.today())

# セーブデータ保存ファイル名
csv_path = "record.csv"

# 🧙‍♂️ セーブ用データ
if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=["日付", "断酒", "運動", "節約額", "ゴールド", "健康", "精神力", "筋力", "かっこよさ"])
    df_init.to_csv(csv_path, index=False)

# CSSデザイン
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

st.title("🎮 断酒クエスト")

# 記録用フラグ
did_abstain = False
did_exercise = False
saved_money = 0

# ✅ 今日断酒した？
if st.button("🍺 今日お酒を我慢しました！"):
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    did_abstain = True
    st.success("断酒成功！ +1500G、健康+1、精神力+1")

# 🧾 今日の食費入力
expense = st.number_input("🧾 今日の食費はいくら？（円）", min_value=0, step=1)
if st.button("💰 節約金額を計算"):
    savings = 1500 - expense
    if savings > 0:
        st.session_state.gold += savings
        st.session_state.health += 1
        saved_money = savings
        st.success(f"{savings}円 節約！ +{savings}G、健康+1")
    else:
        st.info("今日は節約できなかったみたい…")

# 🏋️ 今日運動した？
if st.button("🏋️ 今日運動しました！"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    did_exercise = True
    st.success("トレーニング完了！ 筋力+1、かっこよさ+1")

# ✅ セーブ処理（1日1回だけ記録追加）
if st.button("📥 今日の記録をセーブする"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "断酒": "○" if did_abstain else "",
            "運動": "○" if did_exercise else "",
            "節約額": saved_money,
            "ゴールド": st.session_state.gold,
            "健康": st.session_state.health,
            "精神力": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！📗")
    else:
        st.warning("今日の記録はすでに保存されています！")

# 🧠 ステータス表示
st.markdown("## 🧙‍♂️ ステータス画面")
st.markdown("""
<style>
.stat-table {{
    border: 3px double #888888;
    background-color: #111111;
    color: white;
    padding: 10px;
    font-size: 18px;
    font-family: 'M PLUS Rounded 1c', sans-serif;
    width: fit-content;
}}
.stat-table .row {{
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}}
.stat-table .row span:first-child {{
    margin-right: 20px;
}}
.stat-table .row span:last-child {{
    text-align: right;
    min-width: 50px;
    display: inline-block;
}}
</style>
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{gold} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span> {health}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span> {mental}</span></div>
  <div class="row"><span>💪 こうげき力</span><span> {strength}</span></div>
  <div class="row"><span>😎 みりょく</span><span> {cool}</span></div>
</div>
""".format(
    gold=st.session_state.gold,
    health=st.session_state.health,
    mental=st.session_state.mental,
    strength=st.session_state.strength,
    cool=st.session_state.cool
), unsafe_allow_html=True)

# 📖 記録表示
st.markdown("## 📖 記録一覧")
df = pd.read_csv("record.csv")
st.dataframe(df)
