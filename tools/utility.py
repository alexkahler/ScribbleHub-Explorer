"""Utility script to help with small functions like loading data, etc.
"""
from urllib.parse import urlparse
from io import BytesIO
import urllib.request
import requests
import random
import pickle

from implicit.als import AlternatingLeastSquares
import streamlit as st
import zstandard
import pandas as pd

from tools import constants

@st.cache_data(show_spinner=False)
def init_data_load(current_page: constants.Pages):
    """Load data based on the current page.

    Args:
        current_page (constants.Pages): The current page the user is in.

    Returns:
        pandas.DataFrame or Tuple: DataFrame of novels or tuple of two elements, first one is a mapping of Collaborative Filtering and second is a DataFrame of novels.
    """
    
    _, col, _ = st.columns([4,2,4])
    with col:
        with st.spinner('Loading novels... (๑>ᴗ<๑)'):
            novels_df = load_novels()
            if current_page == constants.Pages.Main:
                return novels_df
            elif current_page == constants.Pages.Page_1:
                cf_mappings = load_cf_models()
                return cf_mappings, novels_df
            elif current_page == constants.Pages.Page_2:
                return novels_df
            elif current_page == constants.Pages.Page_3:
                return novels_df    

@st.cache_resource(show_spinner=False)
def load_novels():
    """Load and decompress pickled novels data from RecSys.

    Returns:
        pandas.DataFrame: DataFrame of novels.
    """

    return decompress_unpickle("https://github.com/alexkahler/scribbleHub-recsys/blob/master/models/novels.zst?raw=true")

@st.cache_resource
def load_cf_models():
    """Load and decompress pickled Collaborative Filtering mappings data from RecSys.

    Returns:
        dict: Dictionary of Collaborative Filtering mappings data.
    """
    return decompress_unpickle("https://github.com/alexkahler/scribbleHub-recsys/blob/master/models/mappings.zst?raw=true")
 
@st.cache_resource
def load_als():
    """Load Alternating Least Squares model.

    Returns:
        implicit.als.AlternatingLeastSquares: Alternating Least Squares model.
    """
    url = "https://github.com/alexkahler/scribbleHub-recsys/blob/master/models/implicit_model.npz?raw=true"
    response = requests.get(url)
    data = BytesIO(response.content)
    return AlternatingLeastSquares().load(data)

def decompress_unpickle(file_path: str):
    """Decompress and Unpickle binary data.

    Args:
        file_path (str): Path of the file to decompress and unpickle.

    Returns:
        object: Object resulting from unpickling the decompressed binary data.
    """
    
    url = urlparse(file_path)
    if url.scheme:
        print("Opening from URL.")
        with urllib.request.urlopen(file_path) as response:
            compressed_data = response.read()
    else:
        print("Opening from file.")
        with open(file_path, "rb") as f:
            compressed_data = f.read()
    print("Finished fetching data.")
    binary_data = zstandard.decompress(compressed_data)
    obj = pickle.loads(binary_data)
    return obj
    

def init_sessions_state():
    """Initialize Streamlit session state variables.
    """
    
    default_values = {'genres': [], 'tags': [], 'number': 10, 
                      'username': '', 'filter_viewed': False, 
                      'error_count': 0, 'cb_novel': '', 'cf_novel': '', 
                      'user_id': None, 'novel_id': None, 
                      'current_page': 1, 'current_rank':0}
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def dict_tags_to_list(tag_dict: dict, key: str):
    """Convert dictionary of tags into a list of strings.

    Args:
        tag_dict (dict): Dictionary of tags.
        key (str): Key of the tag data.

    Returns:
        list: List of strings of tags.
    """
    
    if isinstance(tag_dict, list):
        tags = [i[key.strip()] for i in tag_dict]
        return tags
    
    return []
    
def format_tags(tags):
    """Format a list of tags into a string.

    Args:
        tags (list): List of tags.

    Returns:
        str: String of formatted tags separated by " | ".
    """
    
    if tags:
        result = ''
        for i, tag in enumerate(tags):
            result += tag
            
            if i != len(tags) - 1:
                result += ' | '
        
        return result
    return []


def parse_username(username_input: str):
    """Parse username from the input.

    Args:
        username_input (str): The input username.

    Returns:
        int: Parsed username as an integer.
    """
    
    try:
        if not username_input.isdigit():
            username_input = username_input.split("profile/",1)[1]
            username_input = username_input.split('/')[0]
    
        return int(username_input)
     
    except IndexError:
        if error_count("page"):
            st.error(random.choice(constants.USER_PARSE_ERROR))
         
    except:
        if error_count("page"):
            st.error(random.choice(constants.ERROR))
            raise
    st.stop()

def parse_novel_input(novel_input: str):
    """
    Parses the input string to an integer representation of the novel ID.
    
    Args:
        novel_input (str): The input string from the user.

    Returns:
        int: The integer representation of the novel ID.
    """
    
    try:
        if not novel_input.isdigit():
            novel_input = novel_input.split("series/",1)[1]
            novel_input = novel_input.split('/')[0]
        
        return(int(novel_input))
    
    
    #TODO: Clear input upon error by using session_state.username?
    except IndexError:
        if error_count("page"):
            st.error(random.choice(constants.NOVEL_PARSE_ERROR))
    
    except:
        if error_count("page"):
            st.error(random.choice(constants.ERROR))
            raise
    st.stop()
    
    
# TODO: Update argument from user_index to crawled users list.
def is_valid_username(user_id: int, user_index: list):
    """
    Check if a given user ID is valid by checking if it is in the list of crawled users.

    Args:
        user_id (int): The user ID to be checked.
        user_index (list): The list of crawled user IDs.

    Returns:
        bool: True if the user ID is valid, False otherwise.
    """

    if user_id in user_index:
        return True
    return False

def is_valid_novel(novel_id, novels_df):
    """
    Check if a given novel ID is valid by checking if it is in the novels dataframe.
    
    Args:
        novel_id (int): The novel ID to be checked.
        novels_df (pandas.DataFrame): The dataframe containing information about the novels.

    Returns:
        bool: True if the novel ID is valid, False otherwise.
    """
    
    if novel_id in novels_df['novel_id'].values:
        return True   
    return False

def user_input_change(state: str, key: str):
    """
    Updates a session state variable with the value of another session state variable.

    Args:
        state (str): The name of the session state variable to be updated.
        key (str): The name of the session state variable to use as the new value.
    """
    
    # # 1. Access the widget's setting via st.session_state[key]
    # # 2. Set the session state you intended to set in the widget
    # print(f'Storing state: {state} and Key: {key}')
    print(f"State: {state}")
    print(f"Key: {key}")
    st.session_state[state] = st.session_state[key]
    print(st.session_state.get(state))
    

def reset_filters():
    """
    Resets the filter session state variables to their default values.
    """
    
    default_values = {'genres': [], 'tags': [], 'number': 10}
    for key, value in default_values.items():
        st.session_state[key] = value


def sort_recommended_novels(novels: pd.DataFrame, key: str):
    """
    Sorts the given novels dataframe based on the selected sort key.

    Args:
        novels (pandas.DataFrame): The dataframe of novels to be sorted.
        key (str): The session state variable specifying the sort key.

    Returns:
        pandas.DataFrame: The sorted dataframe of novels.
    """
    
    if st.session_state[key] == 'Recommended':
        novels = novels.sort_values(by='score', ascending=False)
    elif st.session_state[key] == "UN's Rating":
        novels = novels.sort_values(by='weighted_rating', ascending=False)
    elif st.session_state[key] == 'Last Update':
        novels = novels.sort_values(by='last_update', ascending=False)
    elif st.session_state[key] == 'Favorites':
        novels = novels.sort_values(by='favorites', ascending=False)
    elif st.session_state[key] == 'Popularity':
        novels = novels.sort_values(by='total_views_all', ascending=False)
    elif st.session_state[key] == 'Readers':
        novels = novels.sort_values(by='readers', ascending=False)
    elif st.session_state[key] == 'Trending':
        novels = novels.sort_values(by='average_views', ascending=False)
    elif st.session_state[key] == 'Chapters':
        novels = novels.sort_values(by='chapters', ascending=False)
    return novels
    
def get_top_novels(novels: pd.Series):
    """
    Filters and sorts a series of novels based on session state filter variables.

    Args:
        novels (pandas.Series): The series of novels to be filtered and sorted.

    Returns:
        pandas.DataFrame: The filtered and sorted dataframe of novels, or None if the series is empty after filtering.
    """
    
    genre_filter = st.session_state.genres
    tags_filter = st.session_state.tags
    if genre_filter:
        novels = novels[novels['genres'].apply(lambda genre : all(item in genre for item in genre_filter))]
    if tags_filter:
        novels = novels[novels['tags'].apply(lambda tag : all(item in tag for item in tags_filter))]
    if novels.empty:
        return None
    with st.spinner('Sorting novels... ≧◡≦'):
        return novels.sort_values(by='weighted_rating', ascending=False).head(100)
      
def error_count(placement: str):
    """
    Keeps track of the number of errors that have occurred and displays an error message if too many errors have occurred.

    Args:
        placement (str): The location where the error message should be displayed ("sidebar" or "page").

    Returns:
        bool: False if too many errors have occurred, True otherwise.
    """
    
    st.session_state['error_count'] += 1
    if st.session_state.error_count > 5:
        if placement == "sidebar":
            st.sidebar.error(random.choice(constants.ERROR_MESSAGE))
        elif placement == "page":
            st.error(random.choice(constants.ERROR_MESSAGE))
        return False
    return True
