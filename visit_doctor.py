import streamlit as st
import sqlite3


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


# CSS Style activated after a success message or error message
try: 
    if flag == 1:
        st.markdown(success_message, unsafe_allow_html= True)
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
