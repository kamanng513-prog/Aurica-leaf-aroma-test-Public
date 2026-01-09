import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows 繁中
rcParams['axes.unicode_minus'] = False

# --- 初始化 session_state ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- 精油類別 & 庫存 ---
class Oil:
    def __init__(self, name, stress, mood, sleep, confidence, spirit):
        self.name = name
        self.properties = {
            "壓力指數": stress,
            "情緒平衡": mood,
            "睡眠品質": sleep,
            "自信心": confidence,
            "精神力": spirit
        }

inventory = [
    Oil("芫荽籽", 6, 7, 4, 8, 7),
    Oil("依蘭依蘭", 8, 9, 7, 10, 4),
    Oil("甜橙", 6, 10, 5, 7, 6),
    Oil("玫瑰草", 7, 8, 6, 6, 5),
    Oil("玫瑰天竺葵", 8, 9, 7, 8, 5),
    Oil("羅馬洋甘菊", 10, 9, 10, 4, 2),
    Oil("真正薰衣草", 10, 8, 10, 4, 3),
    Oil("廣藿香", 8, 7, 6, 5, 4),
    Oil("乳香", 9, 8, 7, 6, 8),
    Oil("茉莉花 ", 7, 10, 6, 10, 5),
    Oil("玫瑰 ", 8, 10, 7, 9, 4),
    Oil("迷迭香", 3, 5, 2, 7, 10),
    Oil("橙花", 9, 9, 8, 9, 4),
    Oil("台灣紅檜", 8, 6, 7, 7, 8),
    Oil("秘魯聖木", 9, 7, 6, 5, 9),
    Oil("香桃木", 7, 7, 6, 6, 6),
    Oil("芳樟木", 7, 6, 7, 5, 6),
    Oil("羅勒", 5, 6, 3, 7, 9),
    Oil("岩蘭草", 10, 8, 10, 5, 6),
    Oil("馬鬱蘭", 9, 7, 9, 4, 4),
    Oil("大西洋雪松", 8, 7, 6, 8, 7),
    Oil("胡椒薄荷", 2, 6, 1, 6, 10),
    Oil("佛手柑", 9, 10, 7, 8, 6),
    Oil("苦橙葉", 8, 8, 6, 7, 5),
    Oil("檀香木", 9, 8, 8, 7, 7),
]

# --- 雷達圖（使用正面療癒標籤）---
def create_radar_chart(user_needs):
    # 正面標籤對應
    positive_labels = {
        "壓力指數": "安全感能量\n(自我放鬆能力)",
        "情緒平衡": "心輪流動\n(情緒穩定度)",
        "睡眠品質": "根基穩定度\n(深層修復力)",
        "自信心": "太陽神經叢力量\n(內在自信)",
        "精神力": "清明覺知力\n(生命活力)"
    }

    categories = [positive_labels[k] for k in user_needs.keys()]
    values = list(user_needs.values())
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='#5E8C61', linewidth=3, linestyle='solid')
    ax.fill(angles, values, color='#A6C4B0', alpha=0.4)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories,fontsize=11,color='#333333')
    ax.tick_params(pad=18)  # 把文字推遠啲
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels([]) # 隱藏數字
    ax.grid(color='gray', alpha=0.3)
    ax.spines['polar'].set_visible(False)

    plt.tight_layout()
    return fig

# --- 暖心訊息 ---
def get_warm_message(user_needs, name):
    primary = max(user_needs, key=user_needs.get)
    messages = {
        "壓力指數": "你最近承擔了許多，需要被溫柔地接住。這組香氣將幫助你放下緊繃，重新感受到內在的安全與平靜。",
        "情緒平衡": "你的心輪正在尋求流動與平衡。這組香氣像溫暖的擁抱，協助情緒自然釋放，找回內心的柔軟與穩定。",
        "睡眠品質": "你的根基需要更深的滋養與修復。這組香氣會帶來大地般的安定感，引導你進入安穩的深層睡眠。",
        "自信心": "你的太陽神經叢正在喚醒內在的力量。這組香氣將強化你的自信光芒，讓你勇敢展現真實的自己。",
        "精神力": "你的覺知力需要被重新點亮。這組香氣帶來清新的生命能量，幫助你恢復專注與活力。"
    }
    body = messages.get(primary, "這組香氣是專為你此刻的狀態調配，願它陪伴你走過這段旅程。")
    return f"親愛的 {name}，\n\n{body}"

# --- 推薦演算法 ---
def calculate_recommendation(user_needs):
    scored = []
    for oil in inventory:
        score = sum(oil.properties[k] * v for k, v in user_needs.items())
        scored.append((oil, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:4] # 前4名

# --- App 頁面 & 美化 ---
st.set_page_config(page_title="Aurica Leaf 香氣情緒療癒測驗", layout="centered")

# 全域淺啡木紋背景 + 整體風格
st.set_page_config(page_title="Aurica Leaf 香氣情緒療癒測驗", layout="centered")

# 全域超淺米色木紋背景 + 文字對比優化
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm00MDYyNDUwLWNsb3NlLXVwLW9mLWxpZ2h0LXdvb2QtZ3JhaW4tdGV4dHVyZS5qcGc.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    .big-title {font-size: 38px !important; text-align: center; color: #3E704D; font-weight: bold; margin-top: 20px; text-shadow: 1px 1px 3px rgba(255,255,255,0.8);}
    .subtitle {font-size: 20px; text-align: center; color: #444;}
    .instruction {font-size: 18px; color: #3E704D; text-align: center; margin: 30px 0;}
    h2, h3 {color: #3E704D !important;}
    .stMarkdown, p, div, label {color: #333 !important;}
    .stButton>button {background-color: #8FB89A; color: white; font-weight: bold; border: none;}
    .stSlider label {color: #333 !important; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# ===== 問題頁共用提示 =====
def show_instruction():
    st.markdown('<div class="instruction">請憑最近一週的感覺選擇<br><strong>1 = 完全不同意　→　5 = 完全同意</strong></div>',
                unsafe_allow_html=True)

# ===== 步驟 0：歡迎頁 =====
if st.session_state.step == 0:
    st.markdown('<div class="big-title">Aurica Leaf<br>專屬香氣情緒療癒測驗</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🌿 聆聽植物的聲音，找回內在的平衡</div>', unsafe_allow_html=True)
    st.markdown("### 🌙 一段為你而設的香氣旅程")
    st.write("在接下來的幾分鐘裡，請放鬆心情，跟隨直覺回答問題。\n植物會傾聽你的狀態，為你調配一組專屬的療癒香氣。")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ 開始測驗", use_container_width=True, type="primary"):
            st.session_state.step = 1
            st.rerun()

# ===== 新步驟 1：輸入名字 =====
elif st.session_state.step == 1:
    st.markdown("### 👋 請告訴我們您的名字")
    st.write("我們會用它來為您客製化專屬訊息，讓療癒更親切。")

    with st.form("name_form"):
        name = st.text_input("您的名字（或暱稱）", placeholder="例如：小明")
        if st.form_submit_button("繼續 →", use_container_width=True):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("請輸入您的名字以繼續。")

# ===== 步驟 2: 壓力指數 =====
elif st.session_state.step == 2:
    st.markdown("### 😰 壓力指數")
    show_instruction()
    with st.form("step2"):
        q1 = st.slider("我最近經常感覺到肩頸緊繃或頭痛，可能是因為壓力太大。", 1, 5, 3, key="s1")
        q2 = st.slider("在日常生活中，我很容易因為小事而感到煩躁或焦慮。", 1, 5, 3, key="s2")
        q3 = st.slider("我常常覺得工作或生活壓力讓我喘不過氣，需要一些方式來放鬆。", 1, 5, 3, key="s3")
        q4 = st.slider("當面對挑戰時，我會感到內心不安或難以平靜下來。", 1, 5, 3, key="s4")
        if st.form_submit_button("下一頁 →", use_container_width=True):
            st.session_state.answers['stress'] = [q1, q2, q3, q4]
            st.session_state.step = 3
            st.rerun()

# ===== 步驟 3: 情緒平衡 =====
elif st.session_state.step == 3:
    st.markdown("### 😔 情緒平衡")
    show_instruction()
    with st.form("step3"):
        q5 = st.slider("我的情緒容易起伏不定，一天內可能從高興變成沮喪。", 1, 5, 3, key="m1")
        q6 = st.slider("我最近常覺得心情低落，需要一些東西來提升正面情緒。", 1, 5, 3, key="m2")
        q7 = st.slider("在人際互動中，我有時會因為情緒不穩而影響到關係。", 1, 5, 3, key="m3")
        q8 = st.slider("我希望能找到方法，讓我的情緒更穩定，不那麼容易被外在影響。", 1, 5, 3, key="m4")
        if st.form_submit_button("下一頁 →", use_container_width=True):
            st.session_state.answers['mood'] = [q5, q6, q7, q8]
            st.session_state.step = 4
            st.rerun()

# ===== 步驟 4: 睡眠品質 =====
elif st.session_state.step == 4:
    st.markdown("### 🌙 睡眠品質")
    show_instruction()
    with st.form("step4"):
        q9 = st.slider("我晚上常常輾轉反側，難以入睡，需要很長時間才能睡著。", 1, 5, 3, key="sl1")
        q10 = st.slider("即使睡覺了，我也經常半夜醒來，導致隔天感覺疲憊。", 1, 5, 3, key="sl2")
        q11 = st.slider("我的睡眠品質不佳，常常覺得休息不夠，影響白天表現。", 1, 5, 3, key="sl3")
        q12 = st.slider("我希望能改善睡眠，讓自己更容易進入深眠狀態。", 1, 5, 3, key="sl4")
        if st.form_submit_button("下一頁 →", use_container_width=True):
            st.session_state.answers['sleep'] = [q9, q10, q11, q12]
            st.session_state.step = 5
            st.rerun()

# ===== 步驟 5: 自信心 =====
elif st.session_state.step == 5:
    st.markdown("### 🙈 自信心")
    show_instruction()
    with st.form("step5"):
        q13 = st.slider("在面對新環境或人時，我常常缺乏自信，覺得自己不夠好。", 1, 5, 3, key="c1")
        q14 = st.slider("我最近覺得自我價值感低，需要一些方式來增強內在力量。", 1, 5, 3, key="c2")
        q15 = st.slider("當需要表達意見時，我有時會猶豫或退縮，不夠勇敢。", 1, 5, 3, key="c3")
        q16 = st.slider("我希望能提升自信，讓自己在工作或生活中更有魅力和決斷力。", 1, 5, 3, key="c4")
        if st.form_submit_button("下一頁 →", use_container_width=True):
            st.session_state.answers['confidence'] = [q13, q14, q15, q16]
            st.session_state.step = 6
            st.rerun()

# ===== 步驟 6: 精神力 =====
elif st.session_state.step == 6:
    st.markdown("### ⚡ 精神力")
    show_instruction()
    with st.form("step6"):
        q17 = st.slider("我白天常常覺得精神不濟，容易分心或無法集中注意力。", 1, 5, 3, key="sp1")
        q18 = st.slider("最近我的活力不足，感覺像缺少動力去完成任務。", 1, 5, 3, key="sp2")
        q19 = st.slider("在忙碌的一天後，我需要一些東西來提振精神，避免疲勞。", 1, 5, 3, key="sp3")
        q20 = st.slider("我希望能增強專注力和精力，讓自己更有效率地處理事務。", 1, 5, 3, key="sp4")
        if st.form_submit_button("🧪 查看我的專屬配方", use_container_width=True, type="primary"):
            st.session_state.answers['spirit'] = [q17, q18, q19, q20]
            st.session_state.step = 7
            st.rerun()

# ===== 步驟 7：結果頁 =====
elif st.session_state.step == 7:
    # 計算平均並轉換 0-10
    avg = lambda lst: sum(lst)/len(lst)
    user_needs = {
        "壓力指數": (avg(st.session_state.answers['stress']) - 1) * 2.5,
        "情緒平衡": (avg(st.session_state.answers['mood']) - 1) * 2.5,
        "睡眠品質": (avg(st.session_state.answers['sleep']) - 1) * 2.5,
        "自信心": (avg(st.session_state.answers['confidence']) - 1) * 2.5,
        "精神力": (avg(st.session_state.answers['spirit']) - 1) * 2.5,
    }

    st.markdown("### 📊 你的療癒地圖")
    st.markdown("#### **你需要被照顧的地方**")
    fig = create_radar_chart(user_needs)
    st.pyplot(fig)

    st.divider()
    st.markdown("### 💌 給你的溫柔訊息")
    st.success(get_warm_message(user_needs, st.session_state.name))

    st.divider()
    st.markdown("### 💧 為你調配的專屬香氣配方")


    top_4 = calculate_recommendation(user_needs)
    total = sum(score for _, score in top_4)

    cols = st.columns(4)
    for i, (oil, score) in enumerate(top_4):
        ratio = score / total * 100
        drops = max(1, round(20 * ratio / 100))
        strong = [k for k, v in oil.properties.items() if v >= 8]
        strong_text = "、".join(strong) if strong else "整體平衡"

        with cols[i]:
            st.markdown(f"**第 {i+1} 名**")
            st.success(oil.name, icon="🌿")
            st.caption(f"強項：{strong_text}")

    st.markdown("---")
    st.markdown("❤️ 這組香氣是專為你此刻的狀態調配，願它陪伴你走過這段旅程。\n**親愛的，你值得被溫柔對待。**")

    if st.button("🔄 重新測驗"):
        st.session_state.clear()
        st.rerun()