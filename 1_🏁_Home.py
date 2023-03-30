import streamlit as st
from utils.color_header_util import colored_header
from utils.emoji_rain_util import rain

st.set_page_config(
    page_title="Streamlit Content Aggregation App",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tony.kipkemboi@snowflake.com',
        'Report a bug': "mailto:tony.kipkemboi@snowflake.com",
        'About': "# This app aggregates content from social meadia based on keyword search and other filters!"
        }
    )

colored_header(
    label="# Aggregate Streamlit Content 🎈",
    description="There's a master Google doc. link at the bottom of this page for Jess!🤗"
)
st.sidebar.success('👆 select options above')
st.markdown("""
Hey! 👋

This app allows you to search for content related to Streamlit (or any other topic) across multiple social media platforms, including YouTube and Twitter. 

The app is designed with the following features:

- Search for YouTube videos related to a specific keyword, with options to filter by date, order the results, and set the maximum number of results.
- Search for tweets related to a specific keyword, with options to set the date range and maximum number of results.
- View and interact with the content from YouTube and Twitter directly within the app.
- Download data from the search results as CSV files.

To get started, simply navigate to the desired social media platform using the sidebar menu. Each page will provide options to customize your search and view the results. 

Happy browsing and Streamlit-ing! 🎈
""")
st.write('---')
st.write("📑 [Google Doc](https://docs.google.com/spreadsheets/d/1BXJb67S0VLekDKiTLn04rL1mKclIZiKXhCIDE33F4Q4/edit#gid=704013770)")
rain(
    emoji="🎈",
    font_size=54,
    falling_speed=8,
    animation_length="infinite",
)
