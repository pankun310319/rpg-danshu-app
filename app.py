import streamlit as st
import pandas as pd
import os
from datetime import date

# ======================
# 【初期設定】
# ======================
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
if 'irihuda_level' not in st.session_state:
    st.session_state.irihuda_level = ""

today = str(date.today())
csv_path = "record.csv"

if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=[
        "日付", "日別効果", "理不尽レベル", "ゴールド", "健康", "精神力", "筋力", "かっこよさ"
    ])
    df_init.to_csv(csv_path, index=False)

df_all = pd.read_csv(csv_path)
if "日別効果" in df_all.columns:
    continuation_days = int((df_all["日別効果"] != "").astype(int).sum())
else:
    continuation_days = 0

def get_level(days):
    if days < 100:
        return int(days / 2)
    elif days < 300:
        return int(50 + (days - 100) * 0.25)
    else:
        return min(99, int(100 + (days - 300) * 0.1))

def get_level_progress(days):
    level = get_level(days)
    if level < 50:
        base = level * 2
    elif level < 100:
        base = 100 + (level - 50) * 4
    else:
        base = 200 + (level - 100) * 10
    return min(100, int((days / (base + 1)) * 100))

level = get_level(continuation_days)
progress = get_level_progress(continuation_days)

# ======================
# 【CSSデザイン】
# ======================
st.markdown("""
<style>
body, .stApp {
    background-color: #000;
    color: white;
}
input, textarea {
    background-color: #111;
    color: white;
    border: 1px solid #888;
    border-radius: 6px;
    padding: 5px;
}
.stButton > button {
    background-color: #222;
    color: white !important;
    font-weight: bold;
    border: 1px solid #888;
    border-radius: 6px;
    padding: 6px 12px;
    margin: 4px 0;
}
.stat-table {
    border: 3px double #888;
    background-color: #111;
    padding: 10px;
    font-size: 18px;
    font-family: 'M PLUS Rounded 1c', sans-serif;
    width: fit-content;
    color: white;
}
.stat-table .row {
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}
.stat-table .row span:first-child { margin-right: 20px; }
.stat-table .row span:last-child {
    text-align: right;
    min-width: 50px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 【UI表示】
# ======================
st.title("🎮 断酒クエスト")

# --- レベル・ステータス表示 ---
st.markdown("## 🧙‍♂️ ステータス画面")
st.markdown(f"🗡 レベル: {level}（続けて {continuation_days} 日）")
st.progress(progress)

st.markdown("""
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

# --- 理不尽モンスター操作 ---
st.header("😡 理不尽モンスター操作")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🙄 弱 (Lv1)"):
        st.session_state.gold += 200
        st.session_state.mental += 1
        st.session_state.irihuda_level = "Lv1"
        st.success("少しイラっとしたけど、よく耐えた！+200G 精神+1")

with col2:
    if st.button("😡 中 (Lv2)"):
        st.session_state.gold += 500
        st.session_state.mental += 2
        st.session_state.irihuda_level = "Lv2"
        st.success("それなりにキツかったけど出し切った！+500G 精神+2")

with col3:
    if st.button("🤬 強 (Lv3)"):
        st.session_state.gold += 1000
        st.session_state.mental += 3
        st.session_state.irihuda_level = "Lv3"
        st.success("不条理の絞め技を勝利でかわした！+1000G 精神+3")

# --- セーブ処理 ---
if st.button("📅 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "理不尽レベル": st.session_state.irihuda_level,
            "ゴールド": st.session_state.gold,
            "健康": st.session_state.health,
            "精神力": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool,
            "日別効果": "理不尽対応"
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！")
    else:
        st.warning("今日は既にセーブされています")

# --- 記録表示 ---
if st.button("📂 記録をひらく"):
    st.markdown("## 📖 記録一覧")
    st.dataframe(df_all, use_container_width=True)
