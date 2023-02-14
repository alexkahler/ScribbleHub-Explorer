#TODO: Specify data type on all function parameters.
#TODO: Write docstring
import streamlit as st
import pandas as pd
import numpy as np

from tools import utility

class CFRecommender():
    """
    A class for Collaborative Filtering Recommendations.
    
    This class is used for generating recommendation results using a specified model for collaborative filtering. 
    The class contains functions for generating similar items, and recommendations for a particular user. 
    Additionally, the class also includes helper functions for processing the recommendation results, 
    applying filters, and scaling the scores.
    
    Attributes:
        model (object): A collaborative filtering model.
        
    """
    
    def __init__(self, model) -> None:
        """
        The constructor for CFRecommender class.
        
        Args:
            model (object): A collaborative filtering model.
            
        """
        
        self.model = model
    
    def similar_items(self, user_id, novel_id, novels, N, cf_mappings):
        """
        Find similar items to a given novel.
        
        This method is used to generate a list of similar items to a given novel based on the user's preferences. 
        The method takes in the user's ID, the novel's ID, the data frame of novels, the number of recommendations 
        desired (N), and the mappings for collaborative filtering. 
        
        Args:
            user_id (int): The ID of the user.
            novel_id (int): The ID of the novel.
            novels (DataFrame): The data frame of novels.
            N (int): The number of recommendations desired.
            cf_mappings (dict): A dictionary containing the mappings for the collaborative filtering.
        
        Returns:
            DataFrame: A data frame of similar items to the given novel, including the novel ID, the score, 
                       and whether the novel has been viewed by the user.
        
        """
        
        novel_to_index = cf_mappings.get('novel_to_index')
        index_to_novel = cf_mappings.get('index_to_novel')
        filter_items = self._apply_filters(novels, novel_to_index, index_to_novel)
        recommendations, scores = self.model.similar_items(novel_to_index[novel_id], N=N+1, items=filter_items, )
        return self._process_recommendation(user_id=user_id, recommendations=recommendations, scores=scores, novels=novels, cf_models=cf_mappings)
       
    def get_recommendations(self, user_id, novels, cf_mappings, N=10):
        """
        Get recommendations for a particular user.
        
        This method is used to generate recommendations for a particular user based on the user's preferences. 
        The method takes in the user's ID, the data frame of novels, the mappings for collaborative filtering, 
        and the number of recommendations desired (N). 
        
        Args:
            user_id (int): The ID of the user.
            novels (DataFrame): The data frame of novels.
            cf_mappings (dict): A dictionary containing the mappings for the collaborative filtering.
            N (int): The number of recommendations desired.
            
        Returns:
            DataFrame: A data frame of recommended novels for the user, including the novel ID, the score, 
                       and whether the novel has been viewed by the user.
        
        """
        
        data = cf_mappings.get('data')
        user_to_index = cf_mappings.get('user_to_index')
        novel_to_index = cf_mappings.get('novel_to_index')
        index_to_novel = cf_mappings.get('index_to_novel')
        filter_items = self._apply_filters(novels, novel_to_index, index_to_novel)
        user_items = data[user_to_index[user_id]]
        try:
            recommendations, scores = self.model.recommend(userid=user_to_index[user_id], user_items=user_items, N=N, filter_already_liked_items=st.session_state.filter_viewed, items=filter_items)
        except ValueError:
            if utility.error_count("page"):
                st.error("Hey! Dial it down a little on those filters. What you're looking for doesn't exist.")
            st.stop()
        return self._process_recommendation(user_id=user_id, recommendations=recommendations, scores=scores, novels=novels, cf_models=cf_mappings)
    
    def _scale_scores(self, scores):
        """
        Scale the scores of the recommended items.
        
        This method is used to scale the scores of the recommended items to a range between 0 and 1. 
        The scores are used to rank the recommendations.
        
        Args:
            scores (list): A list of scores for the recommended items.
        
        Returns:
            list: A list of scaled scores for the recommended items.
        
        """
        
        min_val = 0 # min(scores)
        max_val = max(scores)
        range_val = max_val - min_val
        return [(val - min_val) / range_val for val in scores]
    
    def _process_recommendation(self, user_id, recommendations, scores, novels, cf_models):
        """
        This function processes the recommendation by mapping the indices of the recommended items to their corresponding novel_ids, and storing the results in a dictionary.
        Then, the dictionary is merged with the input `novels` dataframe to include additional information about each novel such as its genres and tags.

        Args:
            user_id (int): The user_id for whom the recommendations are generated.
            recommendations (list of ints): A list of indices of the recommended items.
            scores (list of floats): A list of scores associated with each recommendation.
            novels (pandas dataframe): A dataframe containing information about all the novels.
            cf_models (dict): A dictionary containing 'data', 'user_to_index', and 'index_to_novel' mappings.

        Returns:
            pandas dataframe: A dataframe containing the merged results, with columns 'novel_id', 'score', 'viewed', 'genres', and 'tags'.
        """
        
        data = cf_models.get('data')
        user_to_index = cf_models.get('user_to_index')
        index_to_novel = cf_models.get('index_to_novel')
        results = {}
        scores = self._scale_scores(scores)
        for i, v in enumerate(recommendations):
            rec_index = index_to_novel[v]
            if user_id:
                results[rec_index] = [rec_index, scores[i], np.in1d(recommendations[i], data[user_to_index[user_id]].indices)]
            else:
                results[rec_index] = [rec_index, scores[i], None]
        
        if st.session_state.novel_id in results.keys(): del results[st.session_state.novel_id] # Remove the included recommendation.
                
        merged_df = pd.merge(pd.DataFrame.from_dict(results, orient='index', columns=["novel_id", "score", "viewed"]), novels, on='novel_id') 
        return merged_df
    
    def _apply_filters(self, df, novel_to_index, index_to_novel):
        """
        This function applies filters to the input dataframe based on the values of `genres` and `tags` stored in the `st.session_state` object.
        If the resulting dataframe is not empty, it returns the indices of the filtered items. If the dataframe is empty, it returns None.

        Args:
            df (pandas dataframe): A dataframe containing the processed recommendations.
            novel_to_index (pandas series): A mapping of novel_id to index.
            index_to_novel (pandas series): A mapping of index to novel_id.

        Returns:
            list of ints or None: A list of filtered item indices, or None if the filtered dataframe is empty.
        """

        if st.session_state.genres:
            df = df[df['genres'].apply(lambda genre : all(item in genre for item in st.session_state.genres))]
        if st.session_state.tags:
            df = df[df['tags'].apply(lambda tag : all(item in tag for item in st.session_state.tags))]
        if df.empty:
            return None
        if st.session_state.genres or st.session_state.tags:
            novel_indices = df['novel_id']
            filter_ids = index_to_novel[index_to_novel.isin(novel_indices)]
            items = novel_to_index[filter_ids]
        else:
            items=None
            
        return items
