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

today = str(date.today())
csv_path = "record.csv"

if not os.path.exists(csv_path):
    df_init = pd.DataFrame(columns=[
        "日付", "日別選択", "節約額", "運動",
        "ゴールド", "健康", "精神力", "筋力", "かっこよさ", "日別効果"
    ])
    df_init.to_csv(csv_path, index=False)

# ======================
# 【レベル関連】
# ======================
def get_level(days):
    if days < 100:
        return int(days / 2)  # 0〜49
    elif days < 1095:
        return 50 + int((days - 100) * 49 / (1095 - 100))
    else:
        return 99

def get_level_progress(days):
    if days < 100:
        return int((days % 2) * 50)
    elif days < 1095:
        current = 50 + int((days - 100) * 49 / (1095 - 100))
        next_level = 50 + int(((days + 1) - 100) * 49 / (1095 - 100))
        return int(((days - 100) / (1095 - 100) * 49 - (current - 50)) * 100)
    else:
        return 100

# ======================
# 【CSSデザイン】
# ======================
st.markdown("""
<style>
body, .stApp {
    background-color: #000000;
    color: white;
}
button, .stButton > button {
    background-color: #222;         /* 濃いグレー背景 */
    color: #ffffff !important;      /* はっきりした白文字 */
    font-weight: bold;
    font-size: 16px;
    border: 2px solid #aaa;
    border-radius: 8px;
    padding: 8px 16px;
    margin: 4px 0;
}
input[type="number"], input[type="text"], textarea {
    background-color: #111111;
    color: white;
    border: 1px solid #888;
    padding: 0.5em;
    border-radius: 6px;
label, .stTextInput > label, .stNumberInput > label {
    color: white !important;
}
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
""", unsafe_allow_html=True)

# ======================
# 【UI表示】
# ======================
st.title("🎮 断酒クエスト")
st.header("🍺 今日の断酒状況")

# 🧭 今日の断酒理由（ボタンで選択）
col1, col2 = st.columns(2)
with col1:
    drank_button = st.button("😇 飲まなかった")
with col2:
    defeated_button = st.button("⚔️ 誘惑モンスター撃破！")

# フラグ用
drink_choice = ""
if defeated_button:
    drink_choice = "モンスター撃破"
    st.session_state.gold += 1500
    st.session_state.health += 1
    st.session_state.mental += 1
    st.success("誘惑に勝利！+1500G、健康+1、精神力+1")
elif drank_button:
    drink_choice = "飲まなかった"
    st.session_state.mental += 1
    st.success("シンプルに我慢成功！精神力+1")

# 💴 節約入力
expense = st.number_input("🍱 今日の食費は？（円）", min_value=0, step=1)
saved_money = 0
if st.button("💰 節約を計算"):
    saved_money = 1500 - expense
    if saved_money > 0:
        st.session_state.gold += saved_money
        st.session_state.health += 1
        st.success(f"{saved_money}円 節約！ +{saved_money}G、健康+1")
    else:
        st.info("今日は節約できなかったみたい…")

# 🏃‍♂️ 運動
did_exercise = st.button("🏋️ 運動した")
if did_exercise:
    st.session_state.strength += 1
    st.session_state.cool += 1
    st.success("トレーニング完了！ 筋力+1、かっこよさ+1")

# ✅ セーブ
if st.button("🗓️ 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "日別選択": drink_choice,
            "節約額": saved_money,
            "運動": "○" if did_exercise else "",
            "ゴールド": st.session_state.gold,
            "健康": st.session_state.health,
            "精神力": st.session_state.mental,
            "筋力": st.session_state.strength,
            "かっこよさ": st.session_state.cool,
            "日別効果": "○" if drink_choice else ""
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("セーブ完了！📗")
    else:
        st.warning("今日の記録はすでに保存されています！")

# ======================
# 【ステータス画面】
# ======================
st.markdown("## 🧙‍♂️ ステータス画面")

# レベルと継続日数
df_all = pd.read_csv(csv_path)
if "日別効果" in df_all.columns:
    df_all["連続"] = (df_all["日別効果"] != "").astype(int)
    continuation_days = df_all["連続"].sum()
else:
    continuation_days = 0

level = get_level(continuation_days)
progress = get_level_progress(continuation_days)

st.markdown(f"🏋️ レベル: {level}（続けて {continuation_days} 日）")
st.progress(progress)

# ステータス表
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

# ======================
# 【記録一覧ボタン】
# ======================
if st.button("📖 記録をひらく"):
    df = pd.read_csv(csv_path)
    st.dataframe(df)
