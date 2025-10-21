# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")
st.image("Images/satosugu.jpeg")

# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

csv_data = None
if os.path.exists('data.csv') and os.path.getsize("data.csv") > 0:
    try:
        csv_data = pd.read_csv("data.csv")
        st.success(f"Successfully loaded {len(csv_data)} entries from CSV!")
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
else:
    st.warning("CSV file empty or does not exist yet :(")

json_data = None
if os.path.exists("data.json"):
    try:
        with open("data.json", "r") as file:
            json_data = json.load(file)
        st.success("Successfully loaded JSON data!")
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
else:
    st.warning("JSON file does not exist yet :(")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Genre Distribution") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("This chart displays the count of each anime in each genre from your watchlist.")
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

if csv_data is not None and not csv_data.empty:
    genre_counts = csv_data["Genre"].value_counts()
    st.area_chart(genre_counts)
    st.write(f"Total genres tracked: {len(genre_counts)}")
else:
    st.warning("No CSV data available :( Please add shows to see this graph!")


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Rating Distribution by Status") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Filter anime by their watch status and see how your ratings are distributed. Use the dropdown to select which statuses to include!")
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

if csv_data is not None and not csv_data.empty:
    status_options = csv_data["Status"].unique().tolist()
    selected_statuses = st.multiselect(
        "Select status(es) to display:",
        options = status_options,
        default = status_options
    )

    if "filtered_by_status" not in st.session_state:
        st.session_state.filtered_by_status = csv_data
    
    if selected_statuses:
        filtered_data = csv_data[csv_data["Status"].isin(selected_statuses)]
        st.session_state.filtered_by_status = filtered_data

        rating_counts = filtered_data["Rating"].value_counts().sort_index()
        st.line_chart(rating_counts)
        st.write(f"Displaying {len(filtered_data)} anime")
    else:
        st.info("Please select at least one status to display the graph!")
else:
    st.warning("No CSV data available :( Please add shows to see this graph!")


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Favorite Anime Characters") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Use the slider to set a minimum vote threshold and see which characters are most popular!")
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

if json_data is not None:
    if 'characters' in json_data:
        char_df = pd.DataFrame(json_data["characters"])
        
        max_votes = int(char_df["votes"].max()) if not char_df.empty else 200
        
        min_votes = st.slider( 
            "Minimum Votes:",
            min_value = 0,
            max_value = max_votes,
            value = 0
        )

        if "min_votes_threshold" not in st.session_state: 
            st.session_state.min_votes_threshold = min_votes
        else:
            st.session_state.min_votes_threshold = min_votes

        filtered_chars = char_df[char_df["votes"] >= st.session_state.min_votes_threshold]

        if not filtered_chars.empty:
            chart_data = filtered_chars.set_index("name")["votes"]
            st.bar_chart(chart_data) 
            st.write(f"Showing {len(filtered_chars)} characters with at least {min_votes} votes")
        else: 
            st.info(f"No characters found with votes ≥ {min_votes}")
    else:
        st.warning("JSON data structure not recognized :(")
else:
    st.warning("No JSON data available :(")
