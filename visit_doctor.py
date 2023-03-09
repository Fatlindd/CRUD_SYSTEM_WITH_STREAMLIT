import streamlit as st
import sqlite3


st.title(':male-doctor: Metting with the doctor :female-doctor:')

# Two columns, one for inputs and another one for image
col1, col2 = st.columns(2)

with col1:
    name = st.text_input('Name: ')
    surname = st.text_input('Surname: ')
    email = st.text_input('Email: ')
    date_of_birth = st.date_input('Date of birth: ')
    type_of_visit = st.selectbox(
        'Please enter your type of visit!',
        ('Eye Doctor', 'Dentist', 'Dermatologist', 'Primary Care Provider',)
    )

with col2:
    st.image('doctors.png')

# Four columns for four buttons of CRUD
st.markdown("---")

with col1:
    create = st.button('Create')

with col2:
    read = st.button('Read')

