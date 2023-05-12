import streamlit as st

st.title('Foodie')
st.subheader('Find authentic recipes')

st.text_input(
    label='What nationality of food do you want to cook?',
    help='Japanese, Chinese, French',
)

st.button('Find recipes', key='find')
