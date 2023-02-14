"""
Top 100 ranking based on weighted rating of the novels.
"""
import streamlit as st

from assets import page_elements
from tools import utility
from tools import constants

def main():
    
    novels_df = utility.init_data_load(constants.Pages.Page_2)
    page_elements.sort_by_widget('top_sort')
    top_novels = utility.sort_recommended_novels(utility.get_top_novels(novels_df), 'top_sort')
    page_elements.generate_novel_list(top_novels)     

if __name__ == '__main__':
    st.set_page_config(
        page_title=constants.Pages.Page_2.value.get('page_name', ""),
        page_icon=constants.Pages.Page_2.value.get('icon'),
        layout='wide',
        initial_sidebar_state='collapsed',
        menu_items={
                'Get Help': constants.GET_HELP_URL,
                'Report a bug': constants.REPORT,
                'About': constants.ABOUT_URL
        }
    )

    utility.init_sessions_state()
    page_elements.header(constants.Pages.Page_2)
    page_elements.sidebar_menu(constants.Pages.Page_2)
    main()
    if constants.BUILD == "TEST":
        st.write(st.session_state)