import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# 1. Check if user is already logged in
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 2. Define the login check logic
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "12345":
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Clear password from state
        else:
            st.session_state["authenticated"] = False
            st.error("😕 Access code incorrect")

    if not st.session_state["authenticated"]:
        # Display login input
        st.text_input("Enter Access Code", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True



# 3. Main App Logic
if check_password():
    st.success("Access Granted!")
    st.title("Protected Dashboard")
    # Your protected app content goes here
            # 1. Connect to the SQLite database
    # If the file doesn't exist, this will create an empty one
    conn = sqlite3.connect('survey_results.db')

    # 2. Fetch data directly into a pandas DataFrame
    query = "SELECT * FROM responses"
    df = pd.read_sql(query, conn)



    # 1. Calculate the average
    df["average"] = df.iloc[:, 2:7].mean(axis=1)

    # 2. Define your conditions
    conditions = [
        (df["average"] < 7),
        (df["average"] >= 7) & (df["average"] < 9)
    ]

    # 3. Define the corresponding values
    choices = [1, 2]

    # 4. Apply them (default handles the 'else' case)
    df["morale"] = np.select(conditions, choices, default=3)

    AveragemoraleofTeam = df["morale"].mean()

    st.write("Average Morale of Team:", AveragemoraleofTeam)


    # 3. Close the connection
    conn.close()

    # 4. Display in Streamlit
    st.header("Responses")
    st.dataframe(df,hide_index=True) # Renders an interactive table

    if st.button("Log out"):
        st.session_state["authenticated"] = False
        st.rerun()

    if st.button("Delete survey"):
        conn = sqlite3.connect('survey_results.db')
        c = conn.cursor()
        c.execute('''DELETE FROM responses''')
        conn.commit()
        conn.close()   
        st.rerun()

