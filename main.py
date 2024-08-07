from store.events import EventStore
from account.account_saves import BankAccount
from data_model.model import AccountCreated
import datetime
import streamlit as st




def main():

    st.title("Event Sourcing (Conta Bancária)")

    col1, _ = st.columns([1, 1], gap="large")

    if "event_store" not in st.session_state:
        st.session_state.event_store = EventStore()

    event_store = st.session_state.event_store

    
    with st.expander("Criar Conta"):
        account_id = st.text_input("Account ID")
        owner = st.text_input("Titular da Conta")
        initial_balance = st.number_input("Saldo Inicial")

        if st.button("Criar Conta"):
            account = BankAccount(account_id, owner, initial_balance)
            account_created_event = AccountCreated(datetime.datetime.now(), account_id, owner, initial_balance)
            event_store.save_event(account_created_event)
            st.session_state.account_id = account_id  # Store account ID in session state for later use
            st.success(f"Conta criada para {owner} com o saldo {initial_balance}")

            events = event_store.get_events(account_id)
            print(f"Evento de criação de conta -> {events}")

            if "account" not in st.session_state:
                st.session_state.account = account


    
    with st.expander("Deposito"):

        deposito = st.number_input("Valor do deposito")

        if st.button("Deposito"):
            account = st.session_state.account
            account.deposit(deposito)

            print(f"Transações não comitadas: {account.get_uncommitted_changes()}")

            for event in account.get_uncommitted_changes():
                event_store.save_event(event)
            account.reset_uncommitted_changes()
            st.success(f"O dinheiro foi depositado!")

    with st.expander("Retirada"):

        retirada = st.number_input("Valor da retirada")

        if st.button("Retirada"):
            account = st.session_state.account
            try:
                account.withdraw(retirada)

                print(f"Transações não comitadas: {account.get_uncommitted_changes()}")

                for event in account.get_uncommitted_changes():
                    event_store.save_event(event)
                account.reset_uncommitted_changes()
                st.success(f"O dinheiro foi retirado!")
            except Exception:
                st.error("Saldo Insuficiente!")


    with col1:
        if "account" in st.session_state:
            account_id = st.session_state.account_id 
            events = event_store.get_events(account_id)
            print(f"Eventos -> {events}")
            restored_account = BankAccount.from_events(events)
            st.metric("Saldo", restored_account.balance)


if __name__ == "__main__":
    main()
