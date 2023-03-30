import streamlit as st
from utils.color_header_util import colored_header

if __name__ == '__main__':
    st.set_page_config(
        page_title="Medium Content",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'mailto:tony.kipkemboi@snowflake.com',
            'Report a bug': "mailto:tony.kipkemboi@snowflake.com",
            'About': "# This app aggregates content from social media based on keyword search and other filters!"
        }
    )

    colored_header(
        label="# Aggregate Streamlit Content 🎈",
        description="Maybe we can use CommonRoom instead of re-inventing the wheel here 😅"
    ) 

    st.title("🚧")
    st.info('''💡 Medium does not have an official API for searching articles by keyword.''')