import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide', page_title='COVID-19 Dashboard')

st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 10px;
        background-color: white;
        text-align: center;
        font-size: 14px;
        color: gray;
        border-top: 1px solid #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('./data/covid_19_clean_complete.csv')

df = load_data()

st.markdown('<h1 style="text-align: center;">COVID-19 Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;">Displaying outcome of closed cases and case totals by WHO region</h4>', unsafe_allow_html=True)

latest = df[df['Date'] == df['Date'].max()].copy()
death = latest["Deaths"].sum()
recover = latest["Recovered"].sum()

fig1 = px.pie(
    names=['Recovered', 'Deaths'],
    values=[recover, death],
    title='Outcome of Closed COVID-19 Cases',
    color_discrete_sequence=['#2ecc71', '#e74c3c'])
fig1.update_traces(textinfo='label+percent+value')

reg = latest.groupby('WHO Region')[['Confirmed', 'Deaths', 'Active']].sum()
fig2 = px.imshow(
    reg,
    text_auto=True,
    color_continuous_scale='Reds',
    aspect='auto',
    labels=dict(x='Case Type', y="WHO Region", color='Total Cases'))
fig2.update_layout(title='COVID-19 Cases per WHO Region')

col1, col2 = st.columns(2)
with col1:
    st.subheader('Outcome of Closed Cases')
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.subheader('Case Distribution by Region')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="footer">Made by Daffa 2702376811</div>', unsafe_allow_html=True)
