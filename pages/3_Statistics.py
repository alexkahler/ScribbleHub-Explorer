"""
Statistics page based on the scaped data from ScribbleHub.
"""
import streamlit as st
import pandas as pd

from tools import utility
from tools import constants
from assets import page_elements

#TODO: Refactor similar graphs into functions.
def main():
    
    novels_df = utility.init_data_load(constants.Pages.Page_3)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric('Number of Novels', f"{novels_df['novel_id'].count():,}", help="Number of novels on ScribbleHub in total")
    col2.metric('Number of Authors', f"{novels_df['author_id'].nunique():,}", help="Number of authors on ScribbleHub in total")
    col3.metric('Chapters Published', f"{novels_df['chapters'].sum():,}", help="Total number of chapters published across all novels.")
    col4.metric('Words Written', f"{novels_df['word_count'].sum():,}", help="Total number of words written across all novels.")
    col5.metric('Totals Views', f"{novels_df['total_views_chapters'].sum():,}", help="Total page-views for all novels. This includes non-unique page-views. This is the page-views for all chapters.")
    col6.metric('Number of Readers', f"{novels_df['readers'].sum():,}", help="""A "reader" is a user who has added a novel to their reading list. User's can more than one novel to their reading list, as such, it is not an indicative of the amount of users.""")
    
    metric_expander = st.expander("More Metrics...")
    with metric_expander:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric('Avg. Reviews/Novel', f"{novels_df['reviews_count'].mean():.2f}", help="Average number of reviews per novel.")
        col3.metric('Avg. Chapters/Novel', f"{novels_df['chapters'].mean():.2f}", help="Average number of chapters per novel.")
        col2.metric('Avg. Favorites/Novel', f"{novels_df['favorites'].mean():.2f}", help="""Average number of "favorites" per novel.""")
        col4.metric('Avg. Words/Novel', f"{novels_df['word_count'].mean():,.2f}", help="Average word count across all novels.")
        col5.metric('Avg. Views/Novel', f"{novels_df['total_views_chapters'].mean():,.2f}", help="Average number of chapter views per novel.")
        col6.metric('Avg. Readers/Novel', f"{novels_df['readers'].mean():.2f}", help="Average number users who has added a novel to their reading list.")
        
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Top 15 Most Active Authors')
        active_authors = novels_df.groupby(['author'], as_index=False)['author', 'word_count'].sum('word_count').sort_values(by='word_count', ascending=False).head(15)
        spec = {
            "encoding": {
                "y": {"field": "author", "type": "nominal", "sort":"-x", "axis": {"title": "Author"},},
                "x": {"field": "word_count", "type": "quantitative", "axis": {"title": "Word Count"}},
                "color": {
                    "field": "word_count",
                    "type": "quantitative",
                    "title": "Word Count",
                    "scale": {
                        "domain": [2770236, 5221288],
                        "range": ["#35486D", "#A61F1C"]
                    },
                },
            },
            "mark": "bar"
        }
        st.vega_lite_chart(active_authors, spec=spec, use_container_width=True)
        
        
    with col2:
        col2.write("Novels by Status")  
        status_count = novels_df.groupby(['status'], as_index=False)['novel_id'].count()
        
        spec = {
            'mark': {'type': 'arc', 'tooltip': True, 'innerRadius': 100},
            'encoding': {
                'theta': {'field': 'novel_id', "title":"Count", 'type': 'quantitative'},
                'color': {'field': 'status', 'type': 'nominal', 'title': 'Status','scale':{'range':["#A61F1C", "#564276", "#35486D"] }},
                'text': {'field': 'theta', 'type': 'quantitative'},
            },
        }
        st.vega_lite_chart(status_count, spec=spec, use_container_width=True)
    with col3:
        col3.write("Chapter Distribution (log10 transformed)")
        chapter_count = novels_df.loc[novels_df['chapters'] >= 1]
        spec = {
                "transform": [
                    {
                    "calculate": "log(datum.chapters)/log(10)",
                    "as": "log_chapters"
                    },
                    {
                    "bin": {'binned': True, 'maxbins': 8},
                    "field": "log_chapters",
                    "as": "bin_log_chapters"
                    },
                    {
                    "calculate": "pow(10, datum.bin_log_chapters)",
                    "as": "Chapters (bin start)"
                    },
                    {
                    "calculate": "pow(10, datum.bin_log_chapters_end)",
                    "as": "Chapters (bin end)"
                    }
                ],
                "mark": {"type": "bar", "size":  0.7},
                "encoding": {
                    "x": {
                    "field": "Chapters (bin start)",
                    "scale": {"type": "log", "base": 10},
                    "axis": {"tickCount": 5},
                    },
                    "x2": {"field": "Chapters (bin end)"},
                    "y": {"aggregate": "count", "title": "Number of Novels"},
                    'color': {'value': '#A61F1C'},
                }
        }
        st.vega_lite_chart(chapter_count, spec=spec, use_container_width=True)
        st.caption("* Novels without chapters are excluded.")

    top_tab, best_tab = st.tabs(["Top Genres and Tags", "Best Rated Genres and Tags"])
    
    with top_tab:
        top_tab.subheader("Top Used")
        
        st.write("Top Genres")
        genres_exploded = novels_df.explode('genres')
        genres_exploded['count'] = 1
        genres_formatted = genres_exploded.groupby(['genres', 'status'], as_index=False)['count'].count().sort_values(by='count', ascending=False)
        spec={
            'mark':'bar', 
            'encoding':{
                'y': {
                    ''
                    'field': 'count',
                    'title':'Count',
                    "type": "quantitative",
                    "sort": "-x"
                    },
                'x': {
                    'field': 'genres',
                    'title': 'Genre',
                    'type' : 'nominal',
                    }, 
                'color':{
                    'field': 'status',
                    'title': 'Status',
                    'scale': {
                        'range':["#A61F1C", "#564276", "#35486D"]
                        }
                    },
                'text': {'field': 'count', 'type': 'quantitative'},
                }
            } 
        st.vega_lite_chart(genres_formatted, spec=spec,use_container_width=True)
        
        
        st.write("Top 25 Tags")
        tags_exploded = novels_df.explode('tags')
        tags_exploded['count'] = 1
        tags_grouped = tags_exploded.groupby(['tags', 'status'])['count'].sum().reset_index()
        top_25_tags = tags_grouped.groupby(['tags'])['count'].sum().sort_values(ascending=False).head(25).index
        grouped_filtered = tags_grouped[tags_grouped['tags'].isin(top_25_tags)]
        spec={
            'mark':'bar', 
            'encoding':{
                'y': {
                    'field': 'count',
                    'title':'Count',
                    "type": "quantitative",
                    "sort": "-x"                  },
                'x': {
                    'field': 'tags',
                    'title': 'Tags',
                    'type' : 'nominal',
                    
                    }, 
                'color':{
                    'field': 'status',
                    'title': 'Status',
                    'scale': {
                        'range':["#A61F1C", "#564276", "#35486D"]
                        }
                    }
                }
            } 
        st.vega_lite_chart(grouped_filtered, spec=spec, use_container_width=True)
    
    with best_tab:
        best_tab.subheader("Best Performing")
    
        genres_average = genres_exploded.groupby(['genres'])[['rating', 'rating_votes']].mean().reset_index()
        st.write("Average Rating and Votes by Genre")
        spec = {
            'encoding': {
            "x": {
                            "field": "genres",
                            "type": "nominal",
                            "title": "Genres",
                            "axis": {"title": "Genre"}
                        },
            },
            "layer": [
                {
                    "mark": {"type": "bar", "xOffset": -10, "size":15},# "color": "#A61F1C"},
                    "encoding": {
                        "y": {
                            "field": "rating",
                            "type": "quantitative",
                            "title": "Avg. Rating",
                            "sort": "-x",
                            "axis": {"title": "Avg. Rating", "orient": "left"},
                        },
                        "color": {
                            "field": "rating",
                            "title": "Avg. Rating",
                            "type": "quantitative",
                            "scale": {
                                "range": ["#564276", "#A61F1C"]
                            },
                        },
                        
                    },
                },
                {
                    "mark": {"type": "bar", "xOffset": 10, "size":15, "color": "#35486D"},
                    "encoding": {
                        "y": {
                            "field": "rating_votes",
                            "title": "Avg. Votes",
                            "type": "quantitative",
                            "axis": {"title": "Avg. Votes", "orient": "right"},
                        },
                    },
                },
                
            ], 
            'resolve': {'scale': {'y': 'independent'}}
        }
        st.vega_lite_chart(genres_average, spec=spec, use_container_width=True)
        
        tags_grouped = tags_exploded.groupby(['tags'])[['rating', 'rating_votes']].mean().reset_index().sort_values(by='rating', ascending=False).head(25)
        st.write("Average Rating and Votes by Top 25 Tags")
        spec = {
            'encoding': {
            "x": {
                            "field": "tags",
                            "type": "nominal",
                            "title": "Tags",
                            "axis": {"title": "Tags"}
                        },
            },
            "layer": [
                {
                    "mark": {"type": "bar", "xOffset": -10, "size":15},# "color": "#A61F1C"},
                    "encoding": {
                        "y": {
                            "field": "rating",
                            "type": "quantitative",
                            "title": "Avg. Rating",
                            "axis": {"title": "Avg. Rating", "orient": "left"},
                            "sort": "-x",
                        },
                        "color": {
                            "field": "rating",
                            "title": "Avg. Rating",
                            "type": "quantitative",
                            "scale": {
                                "range": ["#564276", "#A61F1C"]
                            },
                        },
                        
                    },
                },
                {
                    "mark": {"type": "bar", "xOffset": 10, "size":15, "color": "#35486D"},
                    "encoding": {
                        "y": {
                            "field": "rating_votes",
                            "type": "quantitative",
                            "title": "Avg. Votes",
                            "axis": {"title": "Avg. Votes", "orient": "right"}
                        },
                    },
                },
                
            ], 
            'resolve': {'scale': {'y': 'independent'}}
        }
        st.vega_lite_chart(tags_grouped, spec=spec, use_container_width=True)
        
    
    favorites_tab, rating_tab, readers_tab, average_total_views_tab, reviews_tab = st.tabs(["Most Favorited Genre", "Highest Rated Genre", "Genres with Most Readers", "Most Viewed Genres", "Genres with Most Reviews"])
    
    with favorites_tab:
        st.write("Genres that garner the most favorites on average.")
        create_tab_graphs('favorites', 'Avg. Favorites', genres_exploded)
        
    with rating_tab:
        st.write('Average rating of the different genres.')
        create_tab_graphs('rating', 'Avg. Rating', genres_exploded)
        
    with readers_tab:
        st.write("Genres with most readers on average.")
        create_tab_graphs('readers', 'Avg. Readers', genres_exploded)
    
    with average_total_views_tab:
        st.write("Genres that have the most chapter views on average.")
        create_tab_graphs('total_views_chapters', 'Avg. View per Chapter', genres_exploded)
        
    with reviews_tab:
        st.write("Genres that have the most reviews on average.")
        create_tab_graphs('reviews_count', 'Avg. Number of Reviews', genres_exploded)
        
def create_tab_graphs(measure, title, exploded):
    measure_df = exploded.groupby(['genres'], as_index=False)[measure].mean(measure).reset_index().sort_values(by=measure, ascending=False)
    spec = {
    "encoding": {
        "y": {
            "field": measure,
            "type": "quantitative",
            "sort": "-x",
            "axis": {"title": title}
        },
        "x": {
            "field": "genres",
            "type": "nominal",
            "title": "Genres",
        },
        "color": {
            "field": measure,
            "type": "quantitative",
            "title": title,
            "scale": {
                "range": ["#35486D", "#A61F1C"]
            },
        },
    },
    "mark": "bar"
    }
    st.vega_lite_chart(measure_df, spec=spec, use_container_width=True)
    
    # Show user stats - compare it with other users
    # - How many words have been read compared to average other user
    # - How many books in library compared to average other user
    # - Favorite genres
    # - Favorite tags
    # - Amount of followers compared to other users
    # - How do you rate your novels
    # - How do other users rate the same novels
    # - Novel length distribution


if __name__ == '__main__':
    st.set_page_config(
        page_title=constants.Pages.Page_3.value.get('page_name'),
        page_icon=constants.Pages.Page_3.value.get('icon'),
        layout='wide',
        initial_sidebar_state='collapsed',
        menu_items={
                'Get Help': constants.GET_HELP_URL,
                'Report a bug': constants.REPORT,
                'About': constants.ABOUT_URL
        }
    )
    utility.init_sessions_state()
    page_elements.header(constants.Pages.Page_3)
    page_elements.sidebar_menu(constants.Pages.Page_3) 
    main()
    if constants.BUILD == "TEST":
        st.write(st.session_state)
    