#TODO: Specify data type on all function parameters.
#TODO: Write docstring
from pathlib import Path
import random
import textwrap
import base64

from streamlit_extras.colored_header import colored_header
from streamlit.components.v1 import html
import streamlit as st
import pandas as pd

from tools import utility, constants

# Credit to streamlit-extras
def add_logo(logo_url: str, height: int = 125):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6
    The url can either be a url to the image, or a local path to the image.
    
    From streamlit-extras
    
    Args:
        logo_url (str): URL/local path of the logo.
        height (int): Height of the logo.
    """

    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: center 20px;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_username(user_disable = False):
    """Display text input field for username.

    Args:
        user_disable (bool, optional): Toggle whether to disable the field. Defaults to False.
    """
    
    st.sidebar.text_input('User ID or URL', 
                          help=constants.USER_INPUT_HELP, 
                          placeholder=random.choice(constants.USER_ID_SUGGESTIONS), 
                          value=st.session_state.username, 
                          key='username_input', 
                          on_change=utility.user_input_change, 
                          args=('username', 'username_input'), 
                          disabled=user_disable)

def sidebar_menu(current_page: constants.Pages):
    """Display the sidebar menu.
    Menu includes app name, and input fields to filter recommendations.

    Args:
        current_page (constants.Pages): Customize the sidebar based on the currently viewed page.
    """
    
    add_logo("./assets/nuf_chan_x150.png")
    st.sidebar.subheader("ScribbleHub Explorer :telescope:")
    if current_page == constants.Pages.Page_3:
        user_disable = False
        sidebar_username(user_disable)
    elif current_page == constants.Pages.Page_4:
        pass
    else:
        user_disable = False
        number_disable = False
        if current_page == constants.Pages.Main:
            user_disable = True
        elif current_page == constants.Pages.Page_2:
            user_disable = True
            number_disable = False
        sidebar_username(user_disable)
        st.sidebar.multiselect("Filter Genre:",
                               options=constants.FILTER_OPTIONS.get('genres'), 
                               default=st.session_state.genres,
                               help='Filter novels by genre.', 
                               on_change=utility.user_input_change, 
                               key='genres_multi', 
                               args=('genres', 'genres_multi'))
        st.sidebar.multiselect("Filter Tags:", 
                               options=constants.FILTER_OPTIONS.get('tags'),
                               default=st.session_state.tags,
                               help='Filter novels by tags.',
                               on_change=utility.user_input_change, 
                               key='tags_multi',
                               args=('tags', 'tags_multi'))
        # st.sidebar.radio('Filters', ['AND', 'OR'], key='filter_method', label_visibility='collapsed', horizontal=True, disabled=True)
        st.sidebar.slider("Number of Recommendations",
                          value=st.session_state['number'], 
                          min_value=1, max_value=25,
                          help='Number of recommendations to show in recommendedation list.',
                          on_change=utility.user_input_change,
                          key='number_slider',
                          args=('number', 'number_slider'),
                          disabled=number_disable)
        st.sidebar.button('Reset',
                          key='button_reset_filters',
                          help='Remove all filters and reset to default.', 
                          on_click=utility.reset_filters)
    st.sidebar.caption("v.1.0b")

def header(page: constants.Pages):
    """Diplay the page header.

    Args:
        page (constants.Pages): Customize the header based on the currently viewed page.
    """
    
    colored_header(label=page.value.get('title', ""), 
                    color_name="red-80", 
                    description=page.value.get('description', ""))

def sort_by_widget(key: str, show_filter: bool = False):
    """Display the sort-by widget on the main page.

    Args:
        key (str): Key to customize the widget depending on function. Options are 'top_sort' and 'content_sort'.
        show_filter (bool, optional): Toggle whether to show checkbox for filtering viewed novels. Defaults to False.
    """
    
    sort_label, sort_radio, filter_check = st.columns([1,11,2])
    
    sort_label.markdown('**Sort by:**')
    
    if key == 'top_sort':
        options = ["UN's Rating", 
                   'Popularity', 
                   'Favorites', 
                   'Readers',
                   'Chapters',
                   'Last Update',
                   'Trending']
    
    elif key == 'content_sort':
        options = ["UN's Rating",
                   'Recommended',
                   'Popularity',
                   'Favorites',
                   'Readers',
                   'Chapters',
                   'Last Update',
                   'Trending']
    
    else:
        options = ["UN's Rating",
                   'Recommended',
                   'Popularity',
                   'Favorites',
                   'Readers',
                   'Chapters',
                   'Last Update',
                   'Trending']
    
    sort_radio.radio('Sort by:',
                     options=options,
                     horizontal=True,
                     key=key,
                     label_visibility='collapsed')
    
    if show_filter:
        filter_check.checkbox('Filter viewed?', 
                              value=st.session_state.filter_viewed, 
                              help='Filter any novels that you have already added to your reading list.', 
                              key='filter_viewed_check', 
                              on_change=utility.user_input_change, 
                              args=('filter_viewed', 'filter_viewed_check'))
    st.markdown('___')   


def generate_novel_list(recommended_novels: pd.DataFrame):
    """Generates a list of recommendations based on input DataFrame.

    Args:
        recommended_novels (pd.DataFrame): Pandas Dataframe containing recommended novels.
    """
    
    # Rank is the ranking of the novel. We get the current page from the stored session.
    rank = 0 * st.session_state.current_page
    # Figure out how many Novels/Items are in our recommended_novels Dataframe.
    items_amount = len(recommended_novels)
    
    # While the rank is less than the current_page amount and less than the total amount of novels:
    while (rank < (st.session_state.current_page * st.session_state.number) and (rank < items_amount)):
        # Put the novel container on the page.
        novel_container(novel=recommended_novels.iloc[rank], 
                        rank=rank + 1)
        # If the rank is less than the total amount, add 1 to the rank.
        if rank < items_amount:
            rank += 1
        # Else break out of the loop.
        else:
            break
    
    # If the next rank is more than the items amount, disable the "next page" button.
    if rank + 1 > items_amount:
        next_disabled = True
        st.session_state.current_page = 1
    # Else add 1 to our current page, and enable the "next page" button
    else:
        next_disabled = False
        st.session_state.current_page += 1
                
    _, col, _ = st.columns([4,2,3])
    
    if next_disabled: col.caption(random.choice(constants.END_MESSAGE))
    else: col.button('Load More', key='load_more_button', disabled=next_disabled)
    
    # TODO: Attempt at pagination.
    # items_amount = len(recommended_novels)
    # # Calculate the total number of pages based on the number of items and the number of items per page
    # total_pages = math.ceil(items_amount / st.session_state.number)
    # # Get the current page from the stored session
    # current_page = st.session_state.current_page

    # # Check if the current page is within the range of total pages
    # if current_page <= total_pages:
    #     # Get the start and end indices of the items on the current page
    #     start = (current_page - 1) * st.session_state.number
    #     end = current_page * st.session_state.number
    #     # Slice the dataframe to only get the items on the current page
    #     current_page_items = recommended_novels.iloc[start:end]
    #     # Iterate over the items on the current page and put the novel container on the page
    #     for rank, row in enumerate(current_page_items.iterrows(), start=start + 1):
    #         novel_container(novel=row[1], rank=rank)
        
    #     # Enable the "next page" button if the current page is less than the total pages
    #     next_disabled = current_page == total_pages
    #     previous_disable = current_page == 1
    # else:
    #     # If the current page is greater than the total pages, disable the "next page" button
    #     next_disabled = True
    #     previous_disable = False
        
    # col1, _, col2 = st.columns([1,9,1])
    # if col2.button('Next Page', key='next_page_button', disabled=next_disabled):
    #     st.session_state.current_page += 1
    # if col1.button('Previous Page', key='previous_page_button', disabled=previous_disable):
    #     st.session_state.current_page -= 1


  
def novel_container(novel: pd.Series = None, rank: int = 0):
    """
    This function displays a container for a novel using Streamlit. The container includes information about the novel, such as its rank, title, author, synopsis, genres, and other relevant details.
    
    Parameters:
    novel (pd.Series, optional): A pandas series containing the information about the novel. Defaults to None.
    rank (int, optional): The rank of the novel. Defaults to 0.
    
    Returns:
    None
    """
    
    if novel is None:
        return
    
    with st.container():   
        col1, col2 = st.columns([1,11])
        
        with col1:
            col1.markdown("""<style>
                        .stProgress > div > div > div > div {
                            background-image: linear-gradient(to right, #2F4858, #A61F1C);
                        }
                        </style>""", 
                        unsafe_allow_html=True)
            if 'score' in novel: st.progress(float(novel['score']))
            st.image(novel['image_src'])
            col1.markdown(f"""<p style="text-align: center;">{ format(round(novel['weighted_rating'], 1 ), '.1f') } ⭐</p>""", unsafe_allow_html=True) #TODO: Hover-over for precise
        
        with col2:
            
            col2.markdown('##### #{} [{}](https://www.scribblehub.com/series/{})'.format(rank, novel['title'], novel['novel_id']))
            # TODO: Use badges for genres and tags.
            # TODO: Show whether user has seen item.
            if novel['status'] == 'Hiatus - Updated': emoji = ':zzz:'
            elif novel['status'] == 'Completed': emoji = ':white_check_mark:'
            elif novel['status'] == 'Ongoing - Updated': emoji = ':pencil:'
            else: emoji = ':question:'
            col2.caption(f""":sunglasses: *by* [{novel['author']}](https://www.scribblehub.com/profile/{novel['author_id']}) | 
                         :eyes: {novel['total_views_all']} Views | 
                         :heart: {novel['favorites']} Favorites | 
                         :newspaper: {novel['chapters']} Chapters | 
                         :date: {novel['chapters_per_week']} chapters/week | 
                         :eyeglasses: {novel['readers']} Readers | 
                         :scroll: {novel['reviews_count']} Reviews | 
                         :books: {novel['word_count']} Words | 
                         :clock9: { ('N/A'if (novel['last_update'] == 'None') else novel['last_update']) } | 
                         { emoji } {novel['status']}  
                         **Genres**: { utility.format_tags(novel['genres']) }""")
            
            col2.markdown(textwrap.shorten(novel['synopsis'][0], width=350, placeholder='...'), unsafe_allow_html=True)
            
            with st.expander("More >>"): #FIXME: Jumping expander on click.
                st.markdown("###### Synopsis:")
                st.markdown(''.join(novel['synopsis']), unsafe_allow_html=True)
                st.caption(f"""**Tags**: { utility.format_tags(novel['tags']) }""")
        
        st.markdown("___")
        
# Credit to https://extras.streamlit.app/Buy%20Me%20a%20Coffee%20Button
def support_button(floating: bool = True, width: int = 220):
    """
    This function displays a 'Support Me on Ko-fi' button on the Streamlit app.
    
    Parameters:
    - floating (bool, optional): If True, the button will be displayed as a floating button on the bottom-right corner of the app. Default is True.
    - width (int, optional): The width of the button. Default is 220.
    
    Returns:
    None
    """
    
    button = f"""
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
        <script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '#A61F1C', 'B0B2756JF');kofiwidget2.draw();</script> 
    """

    html(button, height=70, width=width)

    if floating:
        st.markdown(
            f"""
            <style>
                iframe[width="{width}"] {{
                    position: fixed;
                    bottom: 60px;
                    right: 40px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )