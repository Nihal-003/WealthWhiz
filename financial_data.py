import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load user details for authentication
def authenticate_user(username, password):
    user_df = pd.read_csv('C:/Users/nidhi/streamlit_project/user_details.csv')
    user = user_df[(user_df['Login'] == username) & (user_df['Password'] == password)]
    return not user.empty

# Load income and expense data, make predictions
def get_financial_summary():
    income_df = pd.read_csv('C:/Users/nidhi/streamlit_project/income.csv')
    expenses_df = pd.read_csv('C:/Users/nidhi/streamlit_project/expenses.csv')

    # Example category mapping
    category_mapping = {
        1: 'Groceries', 2: 'Utilities', 3: 'Transport', 4: 'Dining',
        5: 'Entertainment', 6: 'Healthcare', 7: 'Miscellaneous'
    }

    # Parsing date columns
    income_df['Date'] = pd.to_datetime(income_df['Date'])
    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
    income_df['Month'] = income_df['Date'].dt.to_period('M')
    expenses_df['Month'] = expenses_df['Date'].dt.to_period('M')

    # Merge the data
    merged_data = pd.merge(expenses_df, income_df, on=['UserID', 'Month'], suffixes=('_expense', '_income'))

    # Create lag features
    merged_data['Previous_Month_Expense'] = merged_data.groupby(['UserID', 'CategoryID'])['Amount_expense'].shift(1)
    merged_data.dropna(inplace=True)

    # Prepare data for model training
    X = merged_data[['Amount_income', 'Previous_Month_Expense', 'CategoryID']]
    y = merged_data['Amount_expense']

    # Predict for each category
    predictions = {}
    for category in merged_data['CategoryID'].unique():
        X_cat = X[X['CategoryID'] == category]
        y_cat = y[X['CategoryID'] == category]
        X_train, X_test, y_train, y_test = train_test_split(
            X_cat[['Amount_income', 'Previous_Month_Expense']], y_cat, test_size=0.2, random_state=42)
        model = LinearRegression().fit(X_train, y_train)

        # If there are any test samples, predict for the latest known record
        if not X_test.empty:
            last_known = X_test.iloc[-1:]  # Get the last row of the test data
            predictions[category] = model.predict(last_known[['Amount_income', 'Previous_Month_Expense']])[0]

    # Calculate total expenses and savings
    total_expense = sum(predictions.values())
    total_income = income_df[income_df['Month'] == income_df['Month'].max()]['Amount'].sum()
    total_savings = total_income - total_expense

    return {
        'totalExpenses': total_expense,
        'totalSavings': total_savings,
        'categorizedExpenses': {category_mapping[cat]: amt for cat, amt in predictions.items()},
        'monthlyExpenses': [X['Previous_Month_Expense']]  # Example data, adjust as necessary
    }
