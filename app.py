import streamlit as st
import pandas as pd
import os
from datetime import date

# ======================
# 【初期設定】
# ======================
if 'choice' not in st.session_state:
    st.session_state.choice = ""
if 'irihuda_level' not in st.session_state:
    st.session_state.irihuda_level = ""
if 'saved_money' not in st.session_state:
    st.session_state.saved_money = 0
if 'did_exercise' not in st.session_state:
    st.session_state.did_exercise = False

csv_path = "record.csv"
today = str(date.today())

default_columns = [
    "日付", "日当日", "日常の選択", "日別約", "日別金",
    "健康", "精神", "精神力", "筋力", "かっこよさ",
    "節約額", "運動", "理不尽レベル", "ゴールド", "日別効果"
]

if not os.path.exists(csv_path):
    pd.DataFrame(columns=default_columns).to_csv(csv_path, index=False)

df_all = pd.read_csv(csv_path).fillna(0)
for col in default_columns:
    if col not in df_all.columns:
        df_all[col] = 0

# ======================
# 【レベル計算】
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

def get_days_to_next_level(days):
    level = get_level(days)
    if days < 100:
        next_level_days = (level + 1) * 2
    else:
        next_level_days = 100 + ((level - 49) * 4)
    return max(0, int(next_level_days - days))

# ======================
# 【ステータス累積計算】
# ======================
total_gold = int(df_all["\u30b4\u30fc\u30eb\u30c9"].sum())
total_health = int(df_all["\u5065\u5eb7"].sum())
total_mental = int(df_all["\u7cbe\u795e\u529b"].sum())
total_strength = int(df_all["\u7b4b\u529b"].sum())
total_cool = int(df_all["\u304bっこよさ"].sum())

# ======================
# 【レベルUI】
# ======================
continuation_days = int((df_all["\u65e5\u5225\u52b9\u679c"] != 0).astype(int).sum())
level = get_level(continuation_days)
progress = get_level_progress(continuation_days)
days_to_next = get_days_to_next_level(continuation_days)

st.title("\ud83c\udfae 断酒クエスト")
st.markdown("## \ud83e\uddd9\u200d\u2642\ufe0f ステータス画面")
st.markdown(f"\u30fb\u30ec\u30d9\u30eb: {level} (続けて {continuation_days} 日)  \n\u6b21のレベルまで\uff1a残り{days_to_next}日")
st.progress(progress)

# ======================
# 【累積表示】
# ======================
st.markdown("""
<div class="stat-table">
  <div class="row"><span>\ud83d\udeb0 \u30b4\u30fc\u30eb\u30c9</span><span>{} G</span></div>
  <div class="row"><span>\u2764\ufe0f \u3055\u3044\u3060\u3044HP</span><span>{}</span></div>
  <div class="row"><span>\ud83e\uddd8\u200d\u2642\ufe0f \u3055\u3044\u3060\u3044MP</span><span>{}</span></div>
  <div class="row"><span>\ud83d\udcaa \u3053\u3046\u3052\u304d\u529b</span><span>{}</span></div>
  <div class="row"><span>\ud83d\ude0e \u304b\u3063\u3053\u3088\u3055</span><span>{}</span></div>
</div>
""".format(
    total_gold, total_health, total_mental, total_strength, total_cool
), unsafe_allow_html=True)

# ======================
# 【断酒・節約・運動 入力】
# ======================

st.header("🍺 今日の断酒状況")

col1, col2 = st.columns(2)
with col1:
    if st.button("😇 飲まなかった"):
        st.session_state.choice = "飲まなかった"
        st.session_state.health += 1
        st.success("継続成功！さいだいHP +1")

with col2:
    if st.button("⚔ 誘惑モンスター撃破！"):
        st.session_state.choice = "誘惑モンスター撃破"
        st.session_state.gold += 1500
        st.session_state.health += 1
        st.session_state.mental += 1
        st.success("誘惑に打ち勝った！ +1500G 健康+1 精神+1")

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
# 【理不尽モンスター操作】
# ======================
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

# ======================
# 【セーブ処理】
# ======================
if st.button("📅 今日の結果をセーブ"):
    df = pd.read_csv(csv_path)
    if today not in df["日付"].values:
        new_row = {
            "日付": today,
            "日誌の選択": st.session_state.choice,
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
        st.success("セーブ完了！📗")
    else:
        st.warning("今日は既にセーブ済みです")

# ======================
# 【記録表示】
# ======================
if st.button("📂 記録をひらく"):
    st.markdown("## 📖 記録一覧")
    df_show = pd.read_csv(csv_path)
    st.dataframe(df_show, use_container_width=True)
