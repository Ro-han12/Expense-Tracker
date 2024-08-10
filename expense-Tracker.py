import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description']) 

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expense():
    uploaded_file = st.file_uploader('Choose a file', type=['csv', 'xls', 'xlsx', 'excel'])
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]

        if file_extension == 'csv':
            st.session_state.expenses = pd.read_csv(uploaded_file)
        elif file_extension in ['xls', 'xlsx', 'excel']:
            st.session_state.expenses = pd.read_excel(uploaded_file)
        else:
            st.error('Unsupported file format') 

        st.write(st.session_state.expenses)

# def save_expenses():
#     expenses = st.session_state.expenses

#     # Save as CSV
#     csv_buffer = BytesIO()
#     expenses.to_csv(csv_buffer, index=False)
#     csv_buffer.seek(0)
    
#     st.download_button(
#         label="Download CSV",
#         data=csv_buffer,
#         file_name="expenses.csv",
#         mime="text/csv"
#     )

#     st.success("Expenses saved successfully")
def save_expenses():
    expenses = st.session_state.expenses

    # Save as CSV
    csv_buffer = BytesIO()
    expenses.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Save as PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 12)
    
    # Add title
    text.textLines("Expenses\n")
    
    # Add column headers
    headers = ', '.join(expenses.columns)
    text.textLines(headers)
    
    # Add rows
    for index, row in expenses.iterrows():
        row_text = ', '.join(map(str, row.values))
        text.textLines(row_text)
    
    c.drawText(text)
    c.showPage()
    c.save()
    pdf_buffer.seek(0)

    # Create download links for CSV and PDF files
    st.download_button(
        label="Download CSV",
        data=csv_buffer,
        file_name="expenses.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="expenses.pdf",
        mime="application/pdf"
    )

    st.success("Expenses saved successfully")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning('No expenses to visualize')

st.title("Personalized Expense Tracker")

with st.sidebar:
    st.header("Add Expense")
    date = st.date_input("Date")
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    
    if st.button('Add'):
        add_expense(date, category, amount, description)
        st.success("Expense Added!")

    st.header("File Operations")
    if st.button('Save Expenses'):
        save_expenses()
    if st.button('Load Expenses'):
        load_expense()

st.header('Expenses')
st.write(st.session_state.expenses)

st.header('Visualization')
if st.button('Visualize Expenses'):
    visualize_expenses()
