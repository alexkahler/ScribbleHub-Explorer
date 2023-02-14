"""
User-Item-based Collaborative Filtering from a Implicit dataset.
User can enter their ScribbleHub ID in the sidebar to generate personalized recommendations.
On the second tab, users can enter a Novel ID to get recommendations based on a novel.
"""
import random

import streamlit as st

from tools import constants, utility, cf_engine
from assets import page_elements

def main():
    
    cf_mappings, novels_df = utility.init_data_load(constants.Pages.Page_1)
    cf_recommender = cf_engine.CFRecommender(utility.load_als())
    

    reading_list_tab, similar_novel_tab = st.tabs(['Reading List', 'Similar Novel'])
    
    with reading_list_tab:
        page_elements.sort_by_widget('reading_list_sort', True)
        
        placeholder = reading_list_tab.empty()
        _, col, _ = placeholder.columns([3,3,3])
        
        with col:
            col.caption("""Input your ScribbleHub User ID or URL in the sidebar to start :point_left:  
                                        Or go to the "Find me a similar novel" tab above :point_up:""")
        
        if st.session_state.username != "":
            user_id = utility.parse_username(st.session_state.username)
            
            if utility.is_valid_username(user_id, cf_mappings.get('user_to_index')):
                placeholder.empty()
                
                st.session_state['user_id'] = user_id
                st.session_state['novel_id'] = -1
                
                recommended_novels = cf_recommender.get_recommendations(
                    user_id=st.session_state.user_id, 
                    novels=novels_df, 
                    cf_mappings=cf_mappings, 
                    N=st.session_state.number)
                
                recommended_novels = utility.sort_recommended_novels(
                    recommended_novels,
                    'reading_list_sort')
                
                page_elements.generate_novel_list(recommended_novels)
            else:
                if utility.error_count("page"):
                    st.error(random.choice(constants.UNKNOWN_USER_ERROR))
            
    with similar_novel_tab:
        similar_novel_tab.text_input(value=st.session_state.cf_novel, 
                             placeholder=random.choice(constants.NOVEL_SUGGESTIONS),
                             help=constants.NOVEL_INPUT_HELP,
                             label='ScribbleHub Novel ID or URL',
                             label_visibility='collapsed',
                             key='cf_novel_input',
                             on_change=utility.user_input_change,
                             args=('cf_novel', 'cf_novel_input'))
        
        page_elements.sort_by_widget('novel_tab_sort', False)
        
        placeholder = similar_novel_tab.empty()
        _, col, _ = placeholder.columns([3,3,3])
        
        with col:
            col.caption("""Input a ScribbleHub Novel ID or URL for a novel you like above :point_up:""")
        
        if st.session_state.cf_novel != "":
            novel_id = utility.parse_novel_input(st.session_state.cf_novel)
            
            if utility.is_valid_novel(novel_id, novels_df):
                placeholder.empty()
                
                st.session_state['novel_id'] = novel_id
                
                recommended_novels = cf_recommender.similar_items(
                    user_id=st.session_state.user_id, 
                    novel_id=novel_id, 
                    novels=novels_df, 
                    N=st.session_state.number,
                    cf_mappings=cf_mappings)
                
                recommended_novels = utility.sort_recommended_novels(
                    recommended_novels, 
                    'novel_tab_sort')
                
                page_elements.generate_novel_list(recommended_novels)
            else:
                if utility.error_count("page"):
                    st.error(random.choice(constants.UNKNOWN_NOVEL_ERROR))
      
if __name__ == '__main__':
    
    st.set_page_config(
        page_title=constants.Pages.Page_1.value.get('page_name'),
        page_icon=constants.Pages.Page_1.value.get('icon'),
        layout='wide',
        initial_sidebar_state='collapsed',
        menu_items={
            'Get Help': constants.GET_HELP_URL,
            'Report a bug': constants.REPORT,
            'About': constants.ABOUT_URL,
        }
    )
    
    utility.init_sessions_state()
    page_elements.header(constants.Pages.Page_1)
    page_elements.sidebar_menu(constants.Pages.Page_1)
    main()
    if constants.BUILD == "TEST":
        st.write(st.session_state)