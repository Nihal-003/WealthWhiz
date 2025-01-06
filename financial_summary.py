import streamlit as st
import pandas as pd
from financial_data import get_financial_summary
from datetime import datetime

def calculate_monthly_expenses(summary):
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Create a list to hold monthly expenses
    monthly_expenses = {}
    
    # Assuming that summary contains monthly expense data,
    # Here is where you would actually calculate total expenses
    # For now, we just simulate some values
    monthly_expenses[f"{current_year}-{current_month:02}"] = summary['totalExpenses']

    # Simulate previous months expenses (replace with your actual calculation logic)
    for i in range(1, 13):
        previous_month = (current_month - i - 1) % 12 + 1
        previous_year = current_year - (current_month - i - 1) // 12
        
        # Placeholder logic for previous months (replace with actual data)
        monthly_expenses[f"{previous_year}-{previous_month:02}"] = summary['totalExpenses'] * (0.9 ** i)  # Example decreasing expenses

    return monthly_expenses

def show_financial_summary():
    st.markdown("<h2 style='text-align: center;'>Financial Summary</h2>", unsafe_allow_html=True)
    
    summary = get_financial_summary()

    # Display categorized expenses in a table format
    st.markdown("### Future Categorized Expenses")
    categorized_expenses = summary['categorizedExpenses']
    expense_df = pd.DataFrame(list(categorized_expenses.items()), columns=['Category', 'Amount'])
    st.table(expense_df)

    # Monthly expense trend
    st.markdown("### Monthly Expenses Trend")

    # Calculate monthly expenses for plotting
    monthly_expenses = calculate_monthly_expenses(summary)

    # Convert the monthly expenses into a DataFrame for plotting
    monthly_expenses_df = pd.DataFrame(list(monthly_expenses.items()), columns=['Month', 'Expenses'])
    monthly_expenses_df['Month'] = pd.to_datetime(monthly_expenses_df['Month'])  # Convert to datetime

    # Debug: check the DataFrame before plotting
    st.write("Monthly Expenses Data:", monthly_expenses_df)

    # Ensure there are values to plot
    if not monthly_expenses_df.empty and monthly_expenses_df['Expenses'].sum() > 0:
        # Plot the monthly expenses trend
        st.line_chart(monthly_expenses_df.set_index('Month')['Expenses'])
    else:
        st.warning("No expenses to display in the chart.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Show Total Expenses and Savings
    st.metric("Total Expenses", f"{summary['totalExpenses']}")
    st.metric("Total Savings", f"{summary['totalSavings']}")

    # Add 'Back to Dashboard' button
    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
