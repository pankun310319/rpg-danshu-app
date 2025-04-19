import streamlit as st
import pandas as pd
import os
from datetime import date

today = str(date.today())

# ======================
# 【初期設定】
# ======================
defaults = {
    'gold': 0, 'health': 0, 'mental': 0, 'strength': 0, 'cool': 0, 'wisdom': 0,
    'choice': "", 'did_exercise': False, 'drink_action_done': False,
    'irihuda_weak': 0, 'irihuda_mid': 0, 'irihuda_strong': 0,
    'expenses': [], 'aerobic_km': 0.0, 'aerobic_steps': 0,
    'reverse_mode': False, 'confirm_mode': None,
    'pending_summary': "", 'pending_date': "", 'last_saved_date': "",
    'mp': 7, 'max_mp': 7, 'last_access': today
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======================
# 【関数：今日の食費を計算】
# ======================
def calculate_today_expense():
    return sum(st.session_state.expenses)

# ======================
# 【CSVファイル読み込み】
# ======================
csv_path = "record.csv"
columns = [
    "日付", "日常の選択", "節約額", "運動（筋トレ）", "有酸素距離(km)", "歩数",
    "理不尽Lv1", "理不尽Lv2", "理不尽Lv3",
    "ゴールド", "健康", "精神力", "筋力", "かっこよさ", "かしこさ", "日別効果"
]
if not os.path.exists(csv_path):
    pd.DataFrame(columns=columns).to_csv(csv_path, index=False)

df_all = pd.read_csv(csv_path)
for col in columns:
    if col not in df_all.columns:
        df_all[col] = 0 if col not in ["日付", "日常の選択", "日別効果", "運動（筋トレ）"] else ""

# ======================
# 【ステータス計算】
# ======================
total_gold = df_all["ゴールド"].sum()
total_health = df_all["健康"].sum()
total_mental = df_all["精神力"].sum()
total_strength = df_all["筋力"].sum()
total_cool = df_all["かっこよさ"].sum()
total_wisdom = df_all["かしこさ"].sum()
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
# 【CSSデザイン（ドラクエ風）】
# ======================
st.markdown("""
<style>
/* 全体背景と文字色 */
html, body, .stApp {
    background-color: #000000 !important;
    color: white !important;
}

/* 入力フォームなどの背景色を暗めに統一 */
input, textarea, .stNumberInput input {
    background-color: #111 !important;
    color: white !important;
    border: 1px solid #888 !important;
    border-radius: 6px;
    padding: 5px;
}
.stNumberInput button {
    background-color: #222 !important;
    color: white !important;
    border: 1px solid #888 !important;
}

/* ボタンの色 */
.stButton > button {
    background-color: #222;
    color: white !important;
    font-weight: bold;
    border: 1px solid #888;
    border-radius: 6px;
    padding: 6px 12px;
    margin: 4px 0;
}

/* ラベルやセレクタの文字色 */
label, .stTextInput > label, .stNumberInput > label, .stSelectbox label {
    color: white !important;
}

/* ステータステーブルのデザイン */
.stat-table {
    border: 2px double #aaa;
    background-color: #0a0f23; /* ドラクエの濃紺 */
    padding: 12px 16px;
    font-size: 18px;
    font-family: 'M PLUS Rounded 1c', sans-serif;
    color: white;
    width: fit-content;
    border-radius: 6px;
    box-shadow: 0 0 6px #222;
}
.stat-table .row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
}
.stat-table .row span:first-child {
    margin-right: 20px;
    color: white;
}
.stat-table .row span:last-child {
    min-width: 50px;
    text-align: right;
    display: inline-block;
    color: #fff57a; /* 黄色 */
}

/* st.infoの文字色も白く強制 */
.css-1t3gfev {
    color: white !important;
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
🗡 レベル: {level}（続けて {continuation_days}日）<br>
次のレベルまであと {next_need} 日
</div>
""", unsafe_allow_html=True)
st.progress(progress)

st.markdown(f"""
<div class="stat-table">
   <div class="row"><span>💰 ゴールド</span><span>{int(total_gold)} G</span></div>
   <div class="row"><span>❤️ さいだいHP</span><span>{int(total_health)}</span></div>
   <div class="row"><span>🧠 かしこさ</span><span>{int(total_wisdom)}</span></div>
   <div class="row"><span>🌀 MP</span><span>{int(st.session_state.mp)} / {int(st.session_state.max_mp)}</span></div>
   <div class="row"><span>💪 こうげき力</span><span>{int(total_strength)}</span></div>
   <div class="row"><span>😎 かっこよさ</span><span>{int(total_cool)}</span></div>
</div>
""", unsafe_allow_html=True)

# ======================
# 【UI：断酒と誘惑モンスター】
# ======================
col1, col2 = st.columns(2)
if col1.button("😇 飲まなかった", key="drink_none"):
    if not st.session_state.drink_action_done:
        st.session_state.choice = "飲まなかった"
        st.session_state.health += 1
        st.session_state.wisdom += 1
        st.session_state.drink_action_done = True
        st.success("『飲まなかった』が記録！ さいだいHP+1 かしこさ+1")
    else:
        st.info("すでに選択されています")

elif col2.button("⚔ 誘惑モンスター撃破", key="drink_defeat"):
    if not st.session_state.drink_action_done:
        st.session_state.choice = "誘惑モンスター撃破"
        st.session_state.gold += 1500
        st.session_state.health += 1
        st.session_state.wisdom += 1
        st.session_state.drink_action_done = True
        st.success("誘惑モンスター撃破！ +1500G さいだいHP+1 かしこさ+1")
    else:
        st.info("すでに選択されています")

# ======================
# 【UI：食費記録】
# ======================
st.markdown("### 🍱 食費の記録（1回ごと）")
expense_input = st.number_input("今回の食費（円）", min_value=0, step=1, key="expense_input")
if st.button("➕ この食費を追加", key="add_expense"):
    st.session_state.expenses.append(expense_input)
    st.success(f"{expense_input}円 を追加しました")

# ======================
# 【UI：運動記録】
# ======================
st.markdown("### 🏃‍♂️ 運動の記録")
col_ex1, col_ex2 = st.columns(2)
if col_ex1.button("🏋️ 筋トレした", key="btn_strength"):
    st.session_state.strength += 1
    st.session_state.cool += 1
    st.session_state.did_exercise = True
    st.success("筋トレ記録！ 筋力+1 かっこよさ+1")

with col_ex2.expander("🚶 有酸素運動"):
    km_input = st.number_input("距離（km）", min_value=0.0, step=0.1, key="aerobic_km")
    steps_input = st.number_input("歩数から入力（1歩=0.0007km）", min_value=0, step=100, key="aerobic_steps")
    if st.button("➕ 有酸素を記録", key="btn_aerobic"):
        if km_input > 0:
            st.session_state.aerobic_km += km_input
            st.success(f"{km_input}km を記録！")
        if steps_input > 0:
            converted_km = round(steps_input * 0.0007, 3)
            st.session_state.aerobic_km += converted_km
            st.session_state.aerobic_steps += steps_input
            st.success(f"{steps_input}歩 = {converted_km}km を記録！")

# ======================
# 【UI：理不尽モンスター討伐（累計）】
# ======================
st.markdown("### 😡 理不尽モンスター討伐")
col_i1, col_i2, col_i3 = st.columns(3)
if col_i1.button("🙄 弱 (Lv1)", key="iri_weak"):
    st.session_state.irihuda_weak += 1
    st.session_state.gold += 200
    st.session_state.mental += 1
    st.success("Lv1 討伐！ +200G 精神+1")
if col_i2.button("😡 中 (Lv2)", key="iri_mid"):
    st.session_state.irihuda_mid += 1
    st.session_state.gold += 500
    st.session_state.mental += 2
    st.success("Lv2 討伐！ +500G 精神+2")
if col_i3.button("🤬 強 (Lv3)", key="iri_strong"):
    st.session_state.irihuda_strong += 1
    st.session_state.gold += 1000
    st.session_state.mental += 3
    st.success("Lv3 討伐！ +1000G 精神+3")

# ======================
# 【UI：記録セーブ/リバース選択】
# ======================
st.markdown("---")
dropdown_option = st.selectbox("📦 記録またはリバースを選択", ["選択してください", "📅 今日の記録をセーブ", "🪄 リバース魔法を使う"], key="record_mode")

# ======================
# 【セーブ処理】
# ======================
def save_record(date_str, mode="normal"):
    df = pd.read_csv(csv_path)
    if date_str in df["日付"].values:
        st.warning("⚠️ この日はすでに記録されています。")
        return
    new_row = {
        "日付": date_str,
        "日常の選択": st.session_state.choice,
        "節約額": 1500 - calculate_today_expense() if calculate_today_expense() < 1500 else 0,
        "運動（筋トレ）": "○" if st.session_state.did_exercise else "",
        "有酸素距離(km)": round(st.session_state.aerobic_km, 2),
        "歩数": st.session_state.aerobic_steps,
        "理不尽Lv1": st.session_state.irihuda_weak,
        "理不尽Lv2": st.session_state.irihuda_mid,
        "理不尽Lv3": st.session_state.irihuda_strong,
        "ゴールド": st.session_state.gold,
        "健康": st.session_state.health,
        "精神力": st.session_state.mental,
        "筋力": st.session_state.strength,
        "かっこよさ": st.session_state.cool,
        "かしこさ": st.session_state.wisdom,
        "日別効果": "リバース記録" if mode == "reverse" else "記録済み"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    st.session_state.last_access = today  # MPの自動回復防止
    st.success(f"{date_str} の記録を保存しました！")

# ======================
# 【確認表示用関数】
# ======================
def confirm_save(summary_text, key_prefix):
    st.markdown("### 📜 記録の確認")
    st.markdown("以下の内容で保存します。よろしいですか？")
    st.info(summary_text)
    col1, col2 = st.columns(2)
    confirm = col1.button("✅ はい", key=f"{key_prefix}_confirm")
    cancel = col2.button("❌ いいえ（しゅうせい）", key=f"{key_prefix}_cancel")
    return confirm and not cancel

# ======================
# 【セーブ or リバース分岐処理】
# ======================
if dropdown_option == "📅 今日の記録をセーブ":
    today_summary = f'''
📅 今日: {today}
断酒：{st.session_state.choice or '未選択'}
今日の食費：{calculate_today_expense()}円
運動：{"筋トレあり" if st.session_state.did_exercise else "なし"} / 有酸素 {round(st.session_state.aerobic_km, 2)}km
理不尽：Lv1×{st.session_state.irihuda_weak} Lv2×{st.session_state.irihuda_mid} Lv3×{st.session_state.irihuda_strong}
'''
    if confirm_save(today_summary, "normal"):
        save_record(today, mode="normal")

elif dropdown_option == "🪄 リバース魔法を使う":
    if st.session_state.mp < 6:
        st.warning(f"MPが足りません（現在のMP: {st.session_state.mp}）")
    else:
        reverse_date = st.date_input("📅 記録したい過去の日付を選んでください")
        reverse_summary = f'''
🪄 リバース対象日: {reverse_date}
断酒：{st.session_state.choice or '未選択'}
食費：{calculate_today_expense()}円
運動：{"筋トレあり" if st.session_state.did_exercise else "なし"} / 有酸素 {round(st.session_state.aerobic_km, 2)}km
理不尽：Lv1×{st.session_state.irihuda_weak} Lv2×{st.session_state.irihuda_mid} Lv3×{st.session_state.irihuda_strong}
'''
        if confirm_save(reverse_summary, "reverse"):
            st.session_state.mp -= 6
            save_record(str(reverse_date), mode="reverse")

# ======================
# 【記録表示】
# ======================
if st.button("📂 記録をひらく"):
    st.markdown("## 📖 記録一覧")
    df_show = pd.read_csv(csv_path)
    st.dataframe(df_show, use_container_width=True)

# ======================
# 【CSVダウンロード】
# ======================
import base64
def download_csv_button(file_path, label="📥 CSVダウンロード"):
    with open(file_path, "rb") as f:
        content = f.read()
    b64 = base64.b64encode(content).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_path}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

download_csv_button("record.csv")



