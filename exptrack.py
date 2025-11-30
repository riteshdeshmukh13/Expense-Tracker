import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="RD Expense Tracker", layout="wide")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# ---------------------- FUNCTIONS ----------------------

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame(
        [[date, category, amount, description]],
        columns=["Date", "Category", "Amount", "Description"]
    )
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_expense], ignore_index=True
    )

def load_expenses():
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)
        st.success("Expenses loaded successfully!")

def save_expenses():
    st.session_state.expenses.to_csv("expenses.csv", index=False)
    st.success("Expenses saved as expenses.csv")

def visualize_expenses():
    if st.session_state.expenses.empty:
        st.warning("No expenses to visualize.")
        return

    fig, ax = plt.subplots()
    sns.barplot(data=st.session_state.expenses, x="Category", y="Amount", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------- UI ----------------------

st.title("RD Expense Tracker")

with st.sidebar:
    st.header("Add Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")

    if st.button("Add Expense"):
        add_expense(date, category, amount, description)
        st.success("Expense Added!")

    st.header("File Operations")
    if st.button("Save Expenses"):
        save_expenses()

    load_expenses()  # File uploader stays visible always

st.header("Expenses Table")
st.write(st.session_state.expenses)

st.header("Visualizations")
if st.button("Visualize Expenses"):
    visualize_expenses()
