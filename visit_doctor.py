import streamlit as st
import sqlite3
from datetime import date


st.title(':male-doctor: Metting with the doctor :female-doctor:')


# connection to database
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()


# Creating tables for clients with 5 columns 
# try:
#     table = '''
#         CREATE TABLE IF NOT EXISTS clients (
#             NAME VARCHAR(255),
#             SURNAME VARCHAR(255),
#             EMAIL VARCHAR(255),
#             DATA_OF_BIRTH TEXT,
#             TYPE_OF_VISIT TEXT
#         );
#     '''
#     cursor.execute(table)
# except sqlite3.Error as e:
#     print(f"Database connection error: {e}")


# min_date and max_date because by default date_input offer  2013 to 2023
# and we have optional parameters to display for example years from 1950 to 2023
min_date = date(1950, 1, 1)
max_date = date(2023, 12, 31)

# Two columns, one for inputs and another one for image
col1, col2 = st.columns(2)
with col1:
    name = st.text_input('Name: ')
    surname = st.text_input('Surname: ')
    email = st.text_input('Email: ')
    date_of_birth = st.date_input('Date of birth: ', value=date.today(), min_value=min_date, max_value=max_date)
    type_of_visit = st.selectbox(
        'Please enter your type of visit!',
        ('Eye Doctor', 'Dentist', 'Dermatologist', 'Primary Care Provider',)
    )


with col2:
    st.image('doctors.png')


# Update method is to populate fields of input when we add email and we want to update
def updateClient(email):
    # Query database for user data based on email
    query = "SELECT * FROM clients WHERE EMAIL = ?"
    cursor.execute(query, (email,))
    result = cursor.fetchone()



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


# readData method is used to read data from database based on email
def readData(email):
    if email == 'all':
        cursor.execute("SELECT * FROM clients")
        data = cursor.fetchall()
        new_data = [
                    {'Name': row[0], 
                     'Surname': row[1], 
                     'Email': row[2], 
                     'Date of birth': row[3], 
                     'Type of visit': row[4]}
        for row in data
    ]
    else: 
        cursor.execute("SELECT * FROM clients WHERE EMAIL=?", (email,))
        data = cursor.fetchall()
        new_data = [
            {'Name': row[0], 'Surname': row[1], 'Email': row[2], 'Date of birth': row[3], 'Type of visit': row[4]}
            for row in data
        ]
    return new_data


def importDataFromFile():
    with open('clients.csv', 'rt') as file:
        rows = file.readlines()
    
    for row in rows:
        value = row.strip().split(',')
        if value[0] != 'name':
            name = value[0]
            surname = value[1]
            email = value[2]
            birthday = value[3]
            typeOfVisit = value[4]
            cursor.execute("INSERT INTO clients VALUES(?, ?, ?, ?, ?)", (name, surname, email, birthday, typeOfVisit))


# Four columns for four buttons of CRUD
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    create = st.button('Create')
    if create:
        if name != "" and surname != "" and email != "" and date_of_birth != "" and type_of_visit != "":
            insertClient(name, surname, email, date_of_birth, type_of_visit)
            conn.commit()
            success_message = "<div class='success_message'>Client was successfully added!</div>"
            flag = 1
        else:
            error_message = "<div class='error_message'>Please all fields are required!</div>"
            flag = 0


with col2:
    read = st.button('Read')
    if read:
        data = readData(email)
        if email != '' or email == 'all':
            flag = 2
        else:
            error_message = "<div class='error_message'>Please 'email' field is necessary!</div>"
            flag = 0


with col3:
    update = st.button('Update')
    if update:
        updateClient(email)


with col4:
    delete = st.button('Delete')
    if delete:
        if email != '':
            deleteClient(email)
            conn.commit()
            success_message = f"<div class='success_message'>Client with email {email} is removed!</div>"
            flag = 1
        else:
            error_message = "<div class='error_message'>Please 'email' field is necessary!</div>"
            flag = 0


with col5:
    file = st.button('Import from file')
    if file:
        importDataFromFile()
        conn.commit()
        success_message = f"<div class='success_message'>File clients.csv is uploaded to database!</div>"
        flag = 1


# CSS Style activated after a success message or error message
try: 
    if flag == 1:
        st.markdown(success_message, unsafe_allow_html= True)
    elif flag == 2:
        st.markdown('---')
        st.table(data)
    else:
        st.markdown(error_message, unsafe_allow_html= True)
except:
    pass

# Adding CSS Style for button with width: 150px and height: auto
button_width = '140px'
st.markdown(
    f'''
    <style>
        div.stButton > button:first-child {{
        width: {button_width};
        height: auto;
        }}

        .error_message {{
        padding: 13px;
        background-color: #F5F5F5;
        color: #CD0000;
        border-radius: 5px;
        }}

        .success_message {{
        padding: 13px;
        background-color: #F5F5F5;
        color: #53A95D;
        border-radius: 5px;
        }}

    </style>
    ''', unsafe_allow_html=True,
)
