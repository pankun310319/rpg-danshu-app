import streamlit as st
import pandas as pd
import os
from datetime import date

# 初期ステータス
for stat in ['gold', 'health', 'mental', 'strength', 'cool']:
    if stat not in st.session_state:
        st.session_state[stat] = 0

today = str(date.today())
csv_path = "record.csv"

# CSVがない場合は初期化
if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=["日付", "日別選択", "日別効果", "節約額", "ゴールド", "健康", "精神力", "筋力", "かっこよさ"])
    df_init.to_csv(csv_path, index=False)

# レベル計算
def get_level(days):
    return min(99, int(days**0.6))

def get_level_progress(days):
    now = get_level(days)
    next_lv = min(99, get_level(days + 1))
    if next_lv == now:
        return 1.0
    return (days - now**(1/0.6)) / (next_lv**(1/0.6) - now**(1/0.6))

# UIデザイン
st.markdown("""
<style>
body, .stApp { background-color: #000; color: white; }
input, textarea { background-color: #222; color: white; border: 1px solid #555; }
button { background-color: #333; color: white; border: 1px solid #888; }
label, .stTextInput > label, .stNumberInput > label { color: white !important; }
.stat-table {
    border: 3px double #888;
    background-color: #111;
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
.stat-table .row span:first-child { margin-right: 20px; }
.stat-table .row span:last-child {
    text-align: right;
    min-width: 50px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# タイトル
st.title("🎮 断酒クエスト")

# 記録読込
df_all = pd.read_csv(csv_path)
df_all["連続"] = (df_all["日別効果"] != "").astype(int)
continuation_days = df_all["連続"].sum()

# ----------------------
# 🧠 飲酒選択
# ----------------------
st.header("🍺 今日の断酒状況")
drink_choice = ""
col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 誘惑モンスター撃破！（飲まなかった）"):
        st.session_state.gold += 1500
        st.session_state.health += 1
        st.session_state.mental += 1
        drink_choice = "誘惑モンスター撃破"
        st.success("誘惑に打ち勝った！ +1500G、健康+1、精神力+1")

with col2:
    if st.button("✋ 今日は飲まなかっただけ"):
        drink_choice = "飲まなかった"
        st.info("記録に残るけど、ステータスは上がらないよ")

# ----------------------
# 食費節約
# ----------------------
expense = st.number_input("🧾 今日の食費はいくら？（円）", min_value=0, step=1)
saved_money = 0
if st.button("💰 節約を計算"):
    saved_money = 1500 - expense
    if saved_money > 0:
        st.session_state.gold += saved_money
        st.session_state.health += 1
        st.success(f"{saved_money}円 節約！ +{saved_money}G、健康+1")
    else:
        st.info("今日は節約できなかったみたい")

# ----------------------
# 運動チェック
# ----------------------
did_exercise = False
if st.button("🏋️ 運動した"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    did_exercise = True
    st.success("筋力+1、かっこよさ+1")

# ----------------------
# セーブ
# ----------------------
if st.button("📅 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "日別選択": drink_choice,
            "日別効果": "○" if drink_choice else "",
            "節約額": saved_money,
            "ゴールド": st.session_state.gold,
            "健康": st.session_state.health,
            "精神力": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！📘")
    else:
        st.warning("今日はすでにセーブされています")

# ----------------------
# ステータス・レベル
# ----------------------
level = get_level(continuation_days)
st.markdown(f"### 🧙‍♂️ レベル: {level}（続けて{continuation_days}日）")
st.progress(get_level_progress(continuation_days))

st.markdown("""
<div class="stat-table">
  <div class="row"><span>💰 ゴールド</span><span>{gold} G</span></div>
  <div class="row"><span>❤️ さいだいHP</span><span>{health}</span></div>
  <div class="row"><span>🧘‍♂️ さいだいMP</span><span>{mental}</span></div>
  <div class="row"><span>💪 こうげき力</span><span>{strength}</span></div>
  <div class="row"><span>😎 かっこよさ</span><span>{cool}</span></div>
</div>
""".format(
    gold=st.session_state.gold,
    health=st.session_state.health,
    mental=st.session_state.mental,
    strength=st.session_state.strength,
    cool=st.session_state.cool
), unsafe_allow_html=True)

# ----------------------
# 記録表示
# ----------------------
st.markdown("## 📖 記録一覧")
st.dataframe(df_all)

