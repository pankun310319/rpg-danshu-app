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
if 'choice' not in st.session_state:
    st.session_state.choice = ""

# CSVと日付設定
csv_path = "record.csv"
today = str(date.today())

# カラム定義
columns = [
    "日付", "日常の選択", "節約額", "運動", "理不尽レベル",
    "ゴールド", "健康", "精神力", "精神", "筋力", "かっこよさ", "日別効果"
]

# CSVがなければ作成
if not os.path.exists(csv_path):
    pd.DataFrame(columns=columns).to_csv(csv_path, index=False)

# CSV読み込み
df_all = pd.read_csv(csv_path)

# 欠けてる列を補筆
for col in columns:
    if col not in df_all.columns:
        df_all[col] = 0 if col in ["ゴールド", "健康", "精神力", "精神", "筋力", "かっこよさ", "節約額"] else ""

# ステータス累積表示
st.session_state.gold = df_all["ゴールド"].sum()
st.session_state.health = df_all["健康"].sum()
st.session_state.mental = df_all["精神力"].sum()
st.session_state.strength = df_all["筋力"].sum()
st.session_state.cool = df_all["かっこよさ"].sum()

# 続けた日数計算
continuation_days = (df_all["日別効果"] != "").sum()

def get_level(days):
    if days == 0:
        return 0
    elif days < 100:
        return int(days * 0.5)
    else:
        return min(99, int(50 + (days - 100) * 0.25))

def get_level_progress(days):
    if days == 0:
        return 0
    elif days < 100:
        return int((days / 100) * 50)
    else:
        return min(100, int(50 + ((days - 100) / 800) * 50))

def get_next_level_info(days):
    now = get_level(days)
    for d in range(days, 5000):
        if get_level(d) > now:
            return d - days
    return "max"

level = get_level(continuation_days)
progress = get_level_progress(continuation_days)
next_need = get_next_level_info(continuation_days)

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
    background-color: #111 !important;
    color: white !important;
    border: 1px solid #888 !important;
    border-radius: 6px;
    padding: 5px;
}
.stNumberInput input {
    background-color: #111 !important;
    color: white !important;
}
.stNumberInput button {
    background-color: #222 !important;
    color: white !important;
    border: 1px solid #888 !important;
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
label, .stTextInput > label, .stNumberInput > label {
    color: white !important;
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
# 【UI：ステータス表示】
# ======================
st.title("🎮 断酒クエスト")
st.markdown("## 🧙‍♂️ ステータス画面")
st.markdown(f"""
<div style='font-size: 22px;'>
🗡 レベル: {level}（続けて {continuation_days} 日）<br>
次のレベルまであと {next_need} 日
</div>
""", unsafe_allow_html=True)
st.progress(progress)

st.markdown(f"""
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{st.session_state.gold} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span>{st.session_state.health}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span>{st.session_state.mental}</span></div>
  <div class="row"><span>💪 こうげき力</span><span>{st.session_state.strength}</span></div>
  <div class="row"><span>😎 かっこよさ</span><span>{st.session_state.cool}</span></div>
</div>
""", unsafe_allow_html=True)

# ======================
# 【UI：断酒と誘惑モンスター】
# ======================
st.header("🍺 今日の断酒状況")
col1, col2 = st.columns(2)
if col1.button("😇 飲まなかった"):
    st.session_state.choice = "飲まなかった"
    st.success("🍃 継続だけでも立派！")
elif col2.button("⚔ 誘惑モンスター撃破！"):
    st.session_state.choice = "誘惑モンスター撃破"
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    st.success("誘惑に勝った！ +1500G 健康+1 精神+1")

(コード前半はそのまま)

# ======================
# 【UI：ステータス表示】
# ======================
st.title("🎮 断酒クエスト")
st.markdown("## 🧙‍♂️ ステータス画面")
st.markdown(f"""
<div style='font-size: 22px;'>
🗡 レベル: {level}（続けて {continuation_days} 日）<br>
次のレベルまであと {next_need} 日
</div>
""", unsafe_allow_html=True)
st.progress(progress)

st.markdown(f"""
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{st.session_state.gold} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span>{st.session_state.health}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span>{st.session_state.mental}</span></div>
  <div class="row"><span>💪 こうげき力</span><span>{st.session_state.strength}</span></div>
  <div class="row"><span>😎 かっこよさ</span><span>{st.session_state.cool}</span></div>
</div>
""", unsafe_allow_html=True)

# ======================
# 【UI：断酒と誘惑モンスター】
# ======================
st.header("🍺 今日の断酒状況")
col1, col2 = st.columns(2)
if col1.button("😇 飲まなかった"):
    st.session_state.choice = "飲まなかった"
    st.success("🍃 継続だけでも立派！")
elif col2.button("⚔ 誘惑モンスター撃破！"):
    st.session_state.choice = "誘惑モンスター撃破"
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    st.success("誘惑に勝った！ +1500G 健康+1 精神+1")
