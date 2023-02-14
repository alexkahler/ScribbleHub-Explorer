"""
Main page of the ScribbleHub Explorer.
Users can generate recommended novels using a Content-Based Recommendation System.
"""
import random

import streamlit as st

from tools import utility, constants, cb_engine
from assets import page_elements

def main():
    
    novels_df = utility.init_data_load(constants.Pages.Main) #Split init_load_data into init_session_state and init_data_load pass back relevant data depending on page.
    novels_df = novels_df[novels_df.chapters > 5].reset_index(drop=True)
    cb_recommender = cb_engine.CBEngine() 
    
    st.text_input(value=st.session_state.cb_novel, 
                  placeholder=random.choice(constants.NOVEL_SUGGESTIONS),
                  help=constants.NOVEL_INPUT_HELP,
                  label=constants.NOVEL_LABEL,
                  label_visibility='collapsed',
                  key="cb_novel_input", 
                  on_change=utility.user_input_change,
                  args=('cb_novel', 'cb_novel_input'))
    
    page_elements.sort_by_widget('content_sort')

    with st.container():
        placeholder = st.empty()
        _, col, _ = placeholder.columns([3,3,3])
        
        with col:
            col.caption("""Input a ScribbleHub Novel ID or URL for a novel you like above :point_up:""")
            
    if st.session_state.cb_novel != "":
        novel_id = utility.parse_novel_input(st.session_state.cb_novel)
        
        if  utility.is_valid_novel(novel_id, novels_df):
            _, col, _ = placeholder.columns([3,2,3])
            
            with col:
                with st.spinner("""Buidling Similarity Matrix.  
                                This may take awhile... (๑>ᴗ<๑) """):
                    similarity_matrix, indices = cb_recommender.fit(novels_df=novels_df)

            placeholder.empty()
            recommended_novels = cb_recommender.recommend(
                novel_id=novel_id, 
                N=st.session_state.number, 
                matrix=similarity_matrix, 
                indices=indices,
                novels_df=novels_df)
            
            recommended_novels = utility.sort_recommended_novels(
                recommended_novels, 
                'content_sort')
            
            page_elements.generate_novel_list(recommended_novels)

if __name__ == '__main__':
    st.set_page_config(
            page_title=constants.Pages.Main.value.get('page_name'),
            page_icon=constants.Pages.Main.value.get('icon'),
            layout='wide',
            initial_sidebar_state='collapsed',
            menu_items={
                'Get Help': constants.GET_HELP_URL,
                'Report a bug': constants.REPORT,
                'About': constants.ABOUT_URL
            }
        )
    utility.init_sessions_state()
    page_elements.header(constants.Pages.Main)
    page_elements.sidebar_menu(constants.Pages.Main)
    main()
    if constants.BUILD == "TEST":
        st.write(st.session_state)