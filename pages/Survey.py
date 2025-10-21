# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("🍥 Watchlist Tracker 🍥")
st.write("Add anime to your watchlist by filling out the form!")
st.divider()

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    title_input = st.text_input("Anime Title:")
    genre_input = st.selectbox("Genre:", ["Shonen", "Shoujo", "Slice of Life", "Fantasy", "Sports", "Thriller", "Comedy"])
    episodes_input = st.number_input("Episodes Watched:", min_value = 0, step = 1)
    rating_input = st.slider("Your rating:", 1, 10, 5)
    status_input = st.selectbox("Status:", ["Watching", "Completed", "Plan to Watch", "Dropped"])

    # The submit button for the form.
    submitted = st.form_submit_button("Add to List")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        if title_input:
            file_exists = os.path.exists("data.csv")
        
            if file_exists:
                existing_data = pd.read_csv("data.csv")
                if title_input in existing_data['Title'].str.lower().values:
                    st.error(f"⚠️ '{title_input}' is already in your watchlist!")
                else:
                    with open("data.csv", "a", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([title_input, genre_input, episodes_input, rating_input, status_input])
                
                    st.success(f"{title_input} has been added to your watchlist!")
                    st.write(f"**Genre:** {genre_input} | **Episodes:** {episodes_input} | **Rating:** {rating_input}/10 | **Status:** {status_input}")
            else:
                with open("data.csv", "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Genre', 'Episodes', 'Rating', 'Status'])
                    writer.writerow([title_input, genre_input, episodes_input, rating_input, status_input])
            
                st.success(f"{title_input} has been added to your watchlist!")
                st.write(f"**Genre:** {genre_input} | **Episodes:** {episodes_input} | **Rating:** {rating_input}/10 | **Status:** {status_input}")
        else:
            st.error("Please enter an anime title before submitting!")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Your Current Watchlist")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)

    col1, col2 = st.columns([3, 1])
    with col1:
        anime_to_remove = st.selectbox("Remove an anime:", options=current_data_df['Title'].tolist(), key="remove_select")
    with col2:
        st.write("") 
        st.write("") 
        if st.button("🗑️ Remove"):
            updated_df = current_data_df[current_data_df['Title'] != anime_to_remove]
            updated_df.to_csv('data.csv', index = False)
            st.success(f"Removed {anime_to_remove}!")
            st.rerun()

else:
    st.warning("Your watchlist is empty :) Add shows to get started!")

st.divider()
st.image("Images/second-years.jpeg")
