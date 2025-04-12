
import streamlit as st

# ステータスの初期化（←ここがないと format() でエラーになる！）
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

st.markdown("""
<style>
/* 全体の背景と文字色を黒＆白に */
body, .stApp {
    background-color: #000000;
    color: white;
}

/* Streamlitのボタンテキストを白に強制 */
.stButton > button {
    color: white !important;
    background-color: #333333;
    border: 1px solid #888;
}

/* 入力フォームやボタンなども背景を黒っぽく */
div[data-testid="stHorizontalBlock"] > div {
    background-color: #111111;
    color: white;
    border-radius: 8px;
    padding: 8px;
}

/* テキストボックスなどの入力欄の背景 */
input, textarea {
    background-color: #222222;
    color: white;
    border: 1px solid #555;
}

/* 数値入力の＋−ボタンも黒く */
button {
    background-color: #333333;
    color: white;
    border: 1px solid #888;
}

/* ラベルの文字（フォーム名など）も白に */
label, .stTextInput > label, .stNumberInput > label {
    color: white !important;
}

/* 入力欄のラベルテキスト（特にStreamlitのバージョンが新しい場合） */
.css-1cpxqw2 {
    color: white !important;
}

/* ボタンの文字も白に強制 */
button {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🎮 断酒クエスト")

# ✅ 今日断酒した？
if st.button("🍺 今日お酒を我慢しました！"):
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    st.success("断酒成功！ +1500G、健康+1、精神力+1")

# 🧾 今日の食費入力
expense = st.number_input("🧾 今日の食費はいくら？（円）", min_value=0, step=1)
if st.button("💰 節約金額を計算"):
    savings = 1500 - expense
    if savings > 0:
        st.session_state.gold += savings
        st.session_state.health += 1
        st.success(f"{savings}円 節約！ +{savings}G、健康+1")
    else:
        st.info("今日は節約できなかったみたい…")

# 🏋️ 今日運動した？
if st.button("🏋️ 今日運動しました！"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    st.success("トレーニング完了！ 筋力+1、かっこよさ+1")

# 🧠 ステータス表示
st.markdown("## 🧙‍♂️ ステータス画面")

st.markdown("""
<style>
.stat-table {{
    border: 3px double #888888;
    background-color: #111111;  /* 黒背景 */
    color: white;               /* 白文字 */
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
