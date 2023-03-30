import requests
import pytz
import pandas as pd
import streamlit as st
import datetime as dt
# from api import API_KEY

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
        "key": st.secrets.yt_api.API_KEY
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
    st.metric(label="Total", value=int(total_uploads), delta=None)

    st.subheader('Uploads per Day (EDT Timezone)')
    st.bar_chart(uploads_per_day.set_index('Date'))


def to_csv(df):
    return df.to_csv().encode('utf-8')


def search_form():
    with st.sidebar:
        st.image('streamlit-logo.png')
        with st.form("search_form"):
            query = st.text_input('Enter Query', value="'Streamlit'",
                                  help="Use single quotes around your query to get results with exact term i.e. 'streamlit' ")
            max_results = st.number_input("Max Results", value=50, min_value=5, max_value=50, help="Max is 50 and default is 5")
            order = st.selectbox("Order by video", ["date", "rating", "relevance", "title", "videoCount", "viewCount"])

            start, end = st.columns(2)
            with start:
                start_date = st.date_input("Start Date", value=dt.date(2023, 1, 1))
            with end:
                end_date = st.date_input("End Date")

            # Add a submit button to the form
            return st.form_submit_button("Submit"), query, max_results, order, start_date, end_date

def display_videos_with_pagination(df, page, videos_per_page):
    """Display videos with pagination.

    Args:
        df (pd.DataFrame): A DataFrame containing video data.
        page (int): The current page number.
        videos_per_page (int): The number of videos to display per page.
    """
    start_index = (page - 1) * videos_per_page
    end_index = start_index + videos_per_page
    videos_to_display = df.iloc[start_index:end_index]

    for _, row in videos_to_display.iterrows():
        with st.container():
            st.video(row['video_url'])
            st.header('Metadata')
            st.write('CREATOR: ', row['channel_name'])
            st.write('PUBLISH DATE: ', row['publish_date'])

    # Display buttons for pagination
    total_pages = (len(df) + videos_per_page - 1) // videos_per_page
    col1, col2, col3 = st.columns(3)
    if page > 1:
        if col1.button("Previous"):
            update_page(page - 1)
    col2.write(f"Page {page} of {total_pages}")
    if page < total_pages:
        if col3.button("Next"):
            update_page(page + 1)

def update_page(new_page):
    """Update the page number in the URL and rerun the app.

    Args:
        new_page (int): The new page number.
    """
    st.experimental_set_query_params(page=new_page)
    st.experimental_rerun()

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
    st.title("Aggregated Streamlit Content 🎈")

    videos_per_page = 5  # Number of videos to display per page
        
    page = int(st.experimental_get_query_params().get("page", [1])[0])

    # Initialize session state variables for form submission and data
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "df" not in st.session_state:
        st.session_state.df = None

    submitted, query, max_results, order, start_date, end_date = search_form()

    if submitted:
        st.session_state.submitted = True

        # Format dates as ISO 8601 strings
        start_date_iso = start_date.isoformat() + "T00:00:00Z"
        end_date_iso = end_date.isoformat() + "T23:59:59Z"

        raw_data = get_videos(query, max_results, order, start_date_iso, end_date_iso)
        df, csv = data_to_df(raw_data)

        # Store the dataframe in session state
        st.session_state.df = df

        tab1, tab2 = st.tabs(['Data', 'Videos'])
        with tab1:
            st.session_state.submitted = True
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
                file_name='content_data.csv',
                mime='text/csv'
            )
        if st.session_state.submitted or st.session_state.df is not None:
            with tab2:
                # Display videos with pagination
                display_videos_with_pagination(st.session_state.df, page, videos_per_page)


