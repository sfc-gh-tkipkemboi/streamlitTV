import requests
import pandas as pd
import streamlit as st
import datetime as dt
from utils.color_header_util import colored_header
from utils.metrics_card_utils import style_metric_cards
from utils.emoji_rain_util import rain

URL = "https://www.googleapis.com/youtube/v3/search"


def get_videos(query: str, max_results: int, order: str, published_after: str, published_before: str) -> dict:
    """Get a list of videos from the YouTube Data API.
    
    Args:
        query (str): The search query to use.
        max_results (int): The maximum number of results to return.
        order (str): The order in which to return the results.
        published_after (str): The start date for the search period (in ISO 8601 format).
        published_before (str): The end date for the search period (in ISO 8601 format).
        
    Returns:
        dict: A dictionary containing the raw video data.
    """
    params = {
        "key": st.secrets.yt_api.API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
        "order": order,
        "publishedAfter": published_after,
        "publishedBefore": published_before
    }
    all_data = []
    while True:
        response = requests.get(URL, params=params)
        data = response.json()

        # Check for errors in the API response
        if 'error' in data:
            error_message = data['error']['message']
            error_code = data['error']['code']
            
            # Invalid API key
            if 'API key not valid' in error_message:
                st.error("The provided API key is not valid. Please check your API key or reach out to Tony Kipkemboi 🤓")
                return {"items": []}
            
            # Rate limit exceeded
            elif error_code == 403 and 'quota' in error_message:
                st.error("API rate limit exceeded. Please wait and try again tomorrow 😭")
                return {"items": []}
            
            # Network issues or unavailable API
            elif error_code == 503:
                st.error("The API is temporarily unavailable. Please try again later 🙁")
                return {"items": []}

            # Generic error message for other cases
            else:
                st.error(f"An error occurred while fetching videos 🫤: {error_message}")
                return {"items": []}
            
        all_data.extend(data['items'])
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
        else:
            break
    return {"items": all_data}


def data_to_df(data: dict) -> pd.DataFrame:
        """Convert raw data from the YouTube Data API to a Pandas DataFrame.

        Args:
            data (dict): The raw data from the YouTube Data API.

        Returns:
            tuple: A tuple containing the original DataFrame and a CSV-formatted DataFrame.
        """
        df = pd.json_normalize(data['items'])

        # Check if 'video_id' column exists in the dataframe
        if 'id.videoId' not in df.columns:
            st.error("🚨 No videos were found for the specified date range.")
            return None, None

        # Rename columns and add video and channel URLs
        df = df.rename(columns={
            'id.videoId': 'video_id',
            'snippet.publishedAt': 'publish_date',
            'snippet.channelId': 'channel_id',
            'snippet.title': 'title',
            'snippet.description': 'description',
            'snippet.channelTitle': 'channel_name'
        })
        df['video_url'] = "https://www.youtube.com/watch?v=" + df['video_id']
        df['channel_url'] = "https://www.youtube.com/channel/" + df['channel_id']

        # Prepare the CSV-formatted DataFrame
        csv = df[['publish_date', 'video_url', 'title', 'description', 'channel_name', 'channel_url']]
        return df, csv


def create_bar_chart(df: pd.DataFrame):
    """Create a bar chart showing the number of video uploads per day (in EDT timezone) and display the total number of videos uploaded.

    Args:
        df (pd.DataFrame): A DataFrame containing video data, including the 'publish_date' column.
    """
    df['publish_date'] = pd.to_datetime(df['publish_date'], utc=True)
    df['publish_date'] = df['publish_date'].dt.tz_convert('US/Eastern')

    uploads_per_day = df.groupby(pd.Grouper(key='publish_date', freq='D'))['video_id'].count().reset_index()
    uploads_per_day.columns = ['Date', 'Uploads']
    total_uploads = uploads_per_day['Uploads'].sum()

    uploads_per_day['Daily Difference'] = uploads_per_day['Uploads'].diff().fillna(0)
    col1,_,_ = st.columns(3)
    col1.metric(label="Total Video Uploads", value=int(total_uploads), delta=None)
    style_metric_cards()

    st.subheader('Uploads per Day (EDT Timezone)')
    st.bar_chart(uploads_per_day.set_index('Date'))


def search_form():
    with st.sidebar:
        st.title(':wave: :red[Start here] 👇',)
        with st.form("search_form"):
            query = st.text_input('Enter Query', value="'Streamlit'",
                                  help="Use single quotes around your query to get results with exact term i.e. 'streamlit' ")
            max_results = st.number_input("Max Results", value=50, min_value=5, max_value=50, help="Max is 50 and default is 5")
            order = st.selectbox("Order by video", ["date", "rating", "relevance", "title", "videoCount", "viewCount"])

            # Get today's date
            today = dt.datetime.now().date()
            
            start, end = st.columns(2)
            with start:
                start_date = st.date_input("Start Date", value=dt.date(2023, 1, 1), max_value=today)
            with end:
                end_date = st.date_input("End Date", max_value=today)

            # Validate the date range
            if start_date > end_date:
                st.error("Invalid date range. Please ensure the start date is earlier than the end date.")
                return None, None, None, None, None, None 

            return st.form_submit_button("Submit"), query, max_results, order, start_date, end_date
        
def to_csv(df):
    return df.to_csv().encode('utf-8')

if __name__ == '__main__':
    st.set_page_config(
        page_title="Streamlit Content Aggregation App",
        page_icon="📺",
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
        description="Modify search query as needed i.e. 'streamlit gpt'"
    )

    submitted, query, max_results, order, start_date, end_date = search_form()

    if submitted:
        rain(
            emoji="🍄",
            font_size=54,
            falling_speed=5,
            animation_length="1",
        )
        # Format dates as ISO 8601 strings
        start_date_iso = start_date.isoformat() + "T00:00:00Z"
        end_date_iso = end_date.isoformat() + "T23:59:59Z"

        with st.spinner("Fetching data from YouTube API..."):
            raw_data = get_videos(query, max_results, order, start_date_iso, end_date_iso)
        
        with st.spinner("Processing data..."):
            df, csv = data_to_df(raw_data)

        if df is not None and csv is not None:
            tab1, tab2 = st.tabs(['Data', 'Videos'])
            with tab1:
                # Uploads per day
                create_bar_chart(df)

                # Show data
                st.subheader('Data from YouTube')
                st.experimental_data_editor(csv, use_container_width=True)

                # Download CSV
                csv_data = to_csv(csv)
                st.download_button(
                    label="Download data as CSV",
                    data=csv_data,
                    file_name='yt_content_data.csv',
                    mime='text/csv',
                )
        
            with tab2:
                for i, row in df.iterrows():
                    with st.container():
                        st.video(row['video_url'])
                        st.subheader('Metadata')
                        st.write('CREATOR: ', row['channel_name'])
                        st.write('PUBLISH DATE: ', row['publish_date'])
            


