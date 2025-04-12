
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
/* 画面全体を黒背景にして文字を白にする */
body {
    background-color: #000000;
    color: white;
}

/* Streamlitの中身を含めた全体に適用 */
html, .css-1d391kg, .css-ffhzg2 {
    background-color: #000000;
    color: white;
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
