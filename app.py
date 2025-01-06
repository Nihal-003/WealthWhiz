import streamlit as st
import pandas as pd
from pages.financial_summary import show_financial_summary
from pages.saving_recommendations import show_saving_recommendations
from financial_data import get_financial_summary, authenticate_user

# Set page config - Must be the very first Streamlit command in the script
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Custom CSS to improve the app's appearance
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom CSS
local_css("style.css")

# Login form function
def login():
    st.markdown("<h1 style='color: #2c3e50;text-align: center;'>WealthWhiz Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<p style='text-align: center;'>Enter your credentials to access the dashboard.</p>", unsafe_allow_html=True)
        with st.form(key="login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
        
        if login_button:
            if username and password:
                # Authenticate using the CSV file
                if authenticate_user(username, password):
                    st.success("Login successful!")
                    st.session_state["logged_in"] = True
                    st.session_state["current_page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please enter both username and password.")

# Dashboard function
def dashboard():
    st.markdown("<h1 style='color: #2c3e50;'>Financial Dashboard</h1>", unsafe_allow_html=True)
    
    summary = get_financial_summary()

    # Financial summary metrics in well-spaced columns
    st.markdown("<h2 style='text-align: center;'>Overview</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"{summary['totalExpenses']}")  # Adjust as necessary
    with col2:
        st.metric("Total Savings", f"{summary['totalSavings']}")
    with col3:
        savings_rate = (summary['totalSavings'] / (summary['totalExpenses'] + summary['totalSavings'])) * 100
        st.metric("Savings Rate", f"{savings_rate:.1f}%")

    # Divider line and quick navigation buttons
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Quick Navigation</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Financial Summary"):
            st.session_state["current_page"] = "financial_summary"
            st.rerun()
    with col2:
        if st.button("View Saving Recommendations"):
            st.session_state["current_page"] = "saving_recommendations"
            st.rerun()

# Main function to control flow
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"
    
    if not st.session_state["logged_in"]:
        login()
    else:
        if st.session_state["current_page"] == "dashboard":
            dashboard()
        elif st.session_state["current_page"] == "financial_summary":
            show_financial_summary()
        elif st.session_state["current_page"] == "saving_recommendations":
            show_saving_recommendations()

if __name__ == "__main__":
    main()
