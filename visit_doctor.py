import streamlit as st
import sqlite3


st.title(':male-doctor: Metting with the doctor :female-doctor:')


# connection to database
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()


# Creating tables for clients with 5 columns 
try:
    table = '''
        CREATE TABLE IF NOT EXIST clients (
            NAME VARCHAR(255),
            SURNAME VARCHAR(255),
            EMAIL VARCHAR(255),
            DATA_OF_BIRTH TEXT,
            TYPE_OF_VISIT TEXT
        );
    '''
    cursor.execute(table)
except sqlite3.Error as e:
    print(f"Database connection error: {e}")



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


# Insert Method to add data into database clients
def insertClient(name, surname, email, date_of_birth, type_of_visit):
    cursor.execute('''
        INSERT INTO clients
        VALUES (?, ?, ?, ?, ?)
    ''', (name, surname, email, date_of_birth, type_of_visit))


# Delete method to delete a record based on email
def deleteClient(email):
    cursor.execute('''
        DELETE FROM clients
        WHERE email=?
    ''', (email,))


# Four columns for four buttons of CRUD
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    create = st.button('Create')

with col2:
    read = st.button('Read')

with col3:
    update = st.button('Update')


with col4:
    delete = st.button('Delete')

with col5:
    file = st.button('Import from file')


# Adding CSS Style for button with width: 150px and height: auto
button_width = '140px'
st.markdown(
    f'''
    <style>
        div.stButton > button:first-child {{
        width: {button_width};
        height: auto;
        }}
    </style>
    ''', unsafe_allow_html=True,
)