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

today = str(date.today())
csv_path = "record.csv"

# 初回作成時のカラム
default_columns = [
    "日付", "日常の選択", "節約額", "運動", "理不尽レベル",
    "ゴールド", "健康", "精神力", "筋力", "かっこよさ", "日別効果"
]

# CSV存在チェック＋読み込み
if not os.path.exists(csv_path):
    pd.DataFrame(columns=default_columns).to_csv(csv_path, index=False)

df_all = pd.read_csv(csv_path)

# 列が足りなければ追加
for col in default_columns:
    if col not in df_all.columns:
        df_all[col] = ""

# ======================
# 【関数：レベル計算】
# ======================
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
# 【UI：断酒入力】
# ======================
st.title("🎮 断酒クエスト")
st.header("🍺 今日の断酒状況")

col1, col2 = st.columns(2)
with col1:
    if st.button("😇 飲まなかった"):
        st.session_state.choice = "飲まなかった"

with col2:
    if st.button("⚔ 誘惑モンスター撃破！"):
        st.session_state.choice = "誘惑モンスター撃破"
        st.session_state.gold += 1500
        st.session_state.health += 1
        st.session_state.mental += 1
        st.success("誘惑に打ち勝った！ +1500G 健康+1 精神+1")

# ======================
# 【UI：節約・運動】
# ======================
expense = st.number_input("🍱 今日の食費は？（円）", min_value=0, step=1)
if st.button("💰 節約を計算"):
    saved = 1500 - expense
    if saved > 0:
        st.session_state.gold += saved
        st.session_state.health += 1
        st.session_state.saved_money = saved
        st.success(f"{saved}円 節約成功！ +{saved}G 健康+1")
    else:
        st.warning("今日は節約できなかったみたい")

if st.button("🏋️ 運動した"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    st.session_state.did_exercise = True
    st.success("運動完了！ 筋力+1 かっこよさ+1")
else:
    st.session_state.did_exercise = False

# ======================
# 【UI：レベル表示】
# ======================
continuation_days = int((df_all["日別効果"] != "").astype(int).sum())
level = get_level(continuation_days)
progress = get_level_progress(continuation_days)

st.markdown("## 🧙‍♂️ ステータス画面")
st.markdown(f"🗡 レベル: {level}（続けて {continuation_days} 日）")
st.progress(progress)

# ======================
# 【ステータス表示】
# ======================
st.markdown("""
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span>{}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span>{}</span></div>
  <div class="row"><span>💪 こうげき力</span><span>{}</span></div>
  <div class="row"><span>😎 かっこよさ</span><span>{}</span></div>
</div>
""".format(
    st.session_state.gold,
    st.session_state.health,
    st.session_state.mental,
    st.session_state.strength,
    st.session_state.cool
), unsafe_allow_html=True)

# ======================
# 【理不尽モンスター操作】
# ======================
st.header("😡 理不尽モンスター操作")
if 'irihuda_level' not in st.session_state:
    st.session_state.irihuda_level = ""

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

# ======================
# 【セーブ処理】
# ======================
if st.button("📅 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "日常の選択": st.session_state.choice,
            "節約額": st.session_state.get("saved_money", 0),
            "運動": "○" if st.session_state.did_exercise else "",
            "理不尽レベル": st.session_state.irihuda_level,
            "ゴールド": st.session_state.gold,
            "健康": st.session_state.health,
            "精神力": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool,
            "日別効果": "記録済み"
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！")
    else:
        st.warning("今日は既にセーブされています")

# ======================
# 【記録表示】
# ======================
if st.button("📂 記録をひらく"):
    st.markdown("## 📖 記録一覧")
    df_show = pd.read_csv(csv_path)
    st.dataframe(df_show, use_container_width=True)
