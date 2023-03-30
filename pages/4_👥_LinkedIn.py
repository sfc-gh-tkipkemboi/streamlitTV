import streamlit as st
from utils.color_header_util import colored_header

if __name__ == '__main__':
    st.set_page_config(
        page_title="LinkedIn Content",
        page_icon="🤓",
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
    st.info('''💡 LinkedIn has a strict API access policy, and it\'s not possible to search for posts by keyword. 
    I may consider to use alternative methods like web scraping to get this data, but also aware that this may violate LinkedIn\'s terms of service.''')