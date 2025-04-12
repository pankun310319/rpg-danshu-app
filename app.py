
import streamlit as st

# セッションステートでステータス保持
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

st.title("🎮 断酒RPGアプリ")

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
exercise = st.checkbox("🏋️ 今日運動しましたか？")
if exercise:
    st.session_state.strength += 1
    st.session_state.cool += 1
    st.success("筋力+1、かっこよさ+1")

# 🧠 ステータス表示
st.markdown("### 🧠 現在のステータス")
st.write(f"💰 ゴールド：{st.session_state.gold} G")
st.write(f"❤️ 健康：{st.session_state.health}")
st.write(f"🧘 精神力：{st.session_state.mental}")
st.write(f"💪 筋力：{st.session_state.strength}")
st.write(f"😎 かっこよさ：{st.session_state.cool}")
