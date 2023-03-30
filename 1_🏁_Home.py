import streamlit as st

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

st.markdown('# Aggregate Streamlit Content 🎈')
st.sidebar.success('Select social media site above.')
st.markdown("""
Hi there! 👋🏾

This app allows you to search for content related to Streamlit (or any other topic) across multiple social media platforms, including YouTube and Twitter. 

The app is designed with the following features:

- Search for YouTube videos related to a specific keyword, with options to filter by date, order the results, and set the maximum number of results.
- Search for tweets related to a specific keyword, with options to set the date range and maximum number of results.
- View and interact with the content from YouTube and Twitter directly within the app.
- Download data from the search results as CSV files.

To get started, simply navigate to the desired social media platform using the sidebar menu. Each page will provide options to customize your search and view the results. 

Happy browsing and Streamlit-ing! 🎈
""")
