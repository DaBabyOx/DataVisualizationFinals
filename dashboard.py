import streamlit as st

st.set_page_config(layout="wide", page_title="HR Dashboard")

# CSS: Hue animation + sticky footer
st.markdown("""
    <style>
    @keyframes hue {
        0% { color: hsl(0, 100%, 50%); }
        25% { color: hsl(90, 100%, 50%); }
        50% { color: hsl(180, 100%, 50%); }
        75% { color: hsl(270, 100%, 50%); }
        100% { color: hsl(360, 100%, 50%); }
    }

    .hue-text {
        font-size: 36px;
        font-weight: bold;
        animation: hue 8s infinite;
        text-align: center;
        margin-bottom: 30px;
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px;
        background-color: white;
        text-align: center;
        font-size: 14px;
        color: gray;
        border-top: 1px solid #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hue-text">Welcome HR-1</div>', unsafe_allow_html=True)
st.subheader("📂 Choose a case below:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Case 1: Covid 19"):
        st.switch_page("pages/case1.py")

with col2:
    if st.button("📈 Case 2: Employee Data"):
        st.switch_page("pages/case2.py")

st.markdown('<div class="footer">Made by Daffa 2702376811</div>', unsafe_allow_html=True)
