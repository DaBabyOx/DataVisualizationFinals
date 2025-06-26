import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout='wide', page_title='Employee Data Dashboard')

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

st.title('Employee Data Dashboard')
st.markdown("Welcome HR-1! Please select a visualization from the dropdown below.")

df = pd.read_csv('./data/merged_employee_data.csv')

opt = [
    'Employee Count by Gender and Type',
    'Histogram of Current Employee Ratings',
    'Top 5 Business Units by Employee Count',
    'Treemap by Business Unit, Gender, and Race',
    'Employee Count by Type (Filtered by Gender)'
]
sel = st.selectbox('Select a Visualization', opt)

if sel == 'Employee Count by Gender and Type':
    st.subheader('Employee Count by Gender per Employee Type')

    cleaned = df.dropna(subset=['EmployeeType', 'GenderCode'])
    grouped = cleaned.groupby(['EmployeeType', 'GenderCode'])['EmpID'].count().reset_index()
    grouped.rename(columns={'EmpID': 'CountofEmpID'}, inplace=True)
    averages = grouped.groupby('EmployeeType')['CountofEmpID'].mean().reset_index()
    averages.rename(columns={'CountofEmpID': 'Average'}, inplace=True)
    plot = pd.merge(grouped, averages, on='EmployeeType')

    employee_types = plot['EmployeeType'].unique()
    cols = min(3, len(employee_types))
    fig, axes = plt.subplots(1, cols, figsize=(6 * cols, 5), sharey=True)

    if cols == 1:
        axes = [axes]

    for i, (etype, subdf) in enumerate(plot.groupby('EmployeeType')):
        ax = axes[i]
        sns.barplot(data=subdf, x='GenderCode', y='CountofEmpID', hue='GenderCode', ax=ax, palette='pastel', legend=False)
        avg = subdf['Average'].iloc[0]
        ax.axhline(avg, ls='--', color='red')
        ax.text(0.5, avg + 5, f'Avg: {int(avg)}', color='red', ha='center')
        for bar in ax.patches:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 5,
                    f'{int(height)}', ha='center', va='bottom')
        ax.set_title(etype)
        ax.set_ylabel("Count")
        ax.set_xlabel("Gender")

    plt.tight_layout()
    st.pyplot(fig)

elif sel == 'Histogram of Current Employee Ratings':
    st.subheader('Histogram of Employee Ratings')

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        fig, ax = plt.subplots(figsize=(3, 2))
        sns.histplot(data=df, x='Current Employee Rating', bins=10, kde=True, ax=ax, color='skyblue')
        ax.set_title("Histogram of Employee Ratings")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        ax.grid(True)
        st.pyplot(fig)

elif sel == 'Top 5 Business Units by Employee Count':
    st.subheader('Top 5 Business Units by Count of EmpID')
    top5 = df['BusinessUnit'].value_counts().nlargest(5).reset_index()
    top5.columns = ['BusinessUnit', 'Count']
    fig = px.bar(top5, x='Count', y='BusinessUnit', orientation='h', text='Count',
                 color='BusinessUnit', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(yaxis=dict(categoryorder='total ascending'),
                      title="Top 5 Business Units by Count of EmpID")
    st.plotly_chart(fig, use_container_width=True)

elif sel == 'Treemap by Business Unit, Gender, and Race':
    st.subheader('Treemap of All Employees Per Business Unit, Divided by Gender, Diversed Through Race')
    grouped = df.groupby(['BusinessUnit', 'GenderCode', 'RaceDesc'])['EmpID'].count().reset_index()
    grouped.rename(columns={'EmpID': 'EmployeeCount'}, inplace=True)
    grouped['All'] = "All Employees"

    fig = px.treemap(
        grouped,
        path=['All', 'BusinessUnit', 'GenderCode', 'RaceDesc'],
        values='EmployeeCount',
        title="Treemap of All Employees Per Business Unit, Divided by Gender, Diversified Through Race")
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, use_container_width=True)

elif sel == 'Employee Count by Type (Filtered by Gender)':
    st.subheader("Employee Count by Type, Filtered by Gender")
    gen = st.selectbox("Select Gender:", df['GenderCode'].dropna().unique())
    filtered = df[df['GenderCode'] == gen]
    gGroup = filtered.groupby('EmployeeType')['EmpID'].count().reset_index()
    gGroup.rename(columns={'EmpID': 'EmployeeCount'}, inplace=True)

    fig = px.bar(gGroup, x='EmployeeType', y='EmployeeCount', text='EmployeeCount',
                 title=f"Employee Count by Type (Gender: {gen})",
                 color='EmployeeType', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="footer">Made by Daffa 2702376811</div>', unsafe_allow_html=True)
