import streamlit as st
from datetime import datetime
import requests
import datetime

# Backend Flask - URL API
API_URL = "http://localhost:5000"

# Funkcja do pobierania transakcji
def get_transactions():
    response = requests.get(f"{API_URL}/transactions")
    if response.status_code == 200:
        return response.json()
    return []

# Funkcja do dodawania transakcji
def add_transaction(amount, type, category, date):
    date_str = date.strftime("%Y-%m-%d")

    response = requests.post(
        f"{API_URL}/add_transaction",
        json={"amount": amount, "type": type, "category": category, "date": date_str}
    )

    if response.status_code == 200:
        try:
            return response.json()  # Spróbuj zdekodować odpowiedź JSON
        except ValueError:
            print("Odpowiedź nie zawiera danych JSON")
            return None  # Zwróć None, jeśli JSON nie jest poprawny
    else:
        print(f"Błąd serwera: {response.status_code}")
        return None

# Interfejs Streamlit
st.title("Budget Manager")
st.subheader("Add a new transaction")

amount = st.number_input("Amount", min_value=0.01, step=0.01)
transaction_type = st.selectbox("Transaction type", ["Income", "Expense"])
category = st.text_input("Category")
date = st.date_input("Date", min_value=datetime.datetime.today())

if st.button("Add Transaction"):
    response = add_transaction(amount, transaction_type, category, date)
    if response:
      st.success("Transaction added successfully" if response.get("success") else "Something went wrong.")
    else:
      st.error("No response received from the server.")

st.subheader("Transaction List")
transactions = get_transactions()

if transactions:
    for trans in transactions:
        st.write(f"{trans['amount']} | {trans['type']} | {trans['category']} | {trans['date']}")
else:
    st.write("No transactions found.")
