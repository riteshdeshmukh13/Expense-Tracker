import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if 'expenses' not in st.session_state:
    st.session_state['expenses'] = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)  

    def load_expenses():
        uploaded_file = st.file_uploader("Choose a file",type=['csv'])
        if uploaded_file is not None:
            st.session_state.expenses = pd.read_csv(uploaded_file)

     def save_expenses():
        st.session_state.expenses.to_csv('expenses.csv', index=False)
        st.success("Expenses saved sucessfully")    

        def visualize_expenses():
            if not st.session_state.expenses.empty:
                fig, ax = plt.subplots()
                sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("No expenses to visualize.")   

    st.title("RD Expense Tracker") 
    with st.sidebar:
        st.header("Add Expense")
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description")

        if st.button("Add"):
           add_expense(date, category, amount, description)
              st.success("Expense Added!")
           st.header("File Operation")
           if st.button('Save Expenses'):
               save_expenses()
              if st.button('Load Expenses'):
               load_expenses()
               st.header('Expenses')
               st.write(st.session_state.expenses)

               st.header("visualizations")
               if st.button('Visualize Expenses'):
                     visualize_expenses()
                   

           