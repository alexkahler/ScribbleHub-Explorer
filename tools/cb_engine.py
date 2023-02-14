#TODO: Specify data type on all function parameters.
#TODO: Write docstring
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, RobustScaler, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import streamlit as st
import pandas as pd
import numpy as np

class CBEngine():        

    def clean_data(self, string_list):
        """Convert list of strings to lower-case and remove spaces between words.
        """
        
        if isinstance(string_list, list):
            return [str.lower(i.replace(' ', '')) for i in string_list]
        else:
            if isinstance(string_list, str):
                return str.lower(string_list.replace(' ', ''))
            else:
                return ''
    
    def create_soup(self, novels_df):
        """Createas a string-soup from columns in the novels dataframe.

        Args:
            df (DataFrame): Novels DataFrame with the columns 'tags', 'author', and 'fandom_tags'

        Returns:
            string: Concatenated 'soup' string of all tags, fandom_tags and author. 
        """
        
        return ' '.join(novels_df['tags']) + ' ' + ' ' + str(novels_df['author']) + ' ' + ' '.join(novels_df['fandom_tags'])

    def recommend(self, novel_id, N, matrix, indices, novels_df):
        """Generate a recommendation.
        
        Okay. Fair warning. It took me stupidly long to figure out how to filter the results based on 
        genres and tags. First tried to filter the cosine similarity matrix. BIG MISTAKE. Don't go down that
        rabbit hole. And then in a Eureka! moment, I thought, "why not just filter the results after being sorted"
        Voila! From idea to implementation was roughly 5 minutes.

        Args:
            novel_id (int): The novel ID used a basis for getting the recommendation.
            matrix (kernel matrix): ndarray of shape (n_samples_X, n_samples_Y).
            indexes (Pandas Series): A Pandas Series object which have the index and the Novel ID.

        Returns:
            DataFrame: List of recommendations.
        """
        
        idx = indices[novel_id]
        matrix_scores = list(enumerate(matrix[idx]))
        matrix_scores = sorted(matrix_scores, key=lambda x: x[1], reverse=True)
        if st.session_state.genres or st.session_state.tags:
            fid = self.apply_filters(novels_df)
            if fid.empty:
                st.error("Yo, dial it down a little on those filters.")
            filtered_index = indices[fid]
            filtered_index = pd.concat([filtered_index, pd.Series(indices[novel_id], dtype=np.int32)], axis=0) #TODO: Try not use pd.Series - set()?
            matrix_scores = np.array(matrix_scores)[np.in1d(np.array(matrix_scores, dtype=np.float16)[:, 0], filtered_index.values)]
            
        N += 1 # Number 1 is always the novel itself.
        matrix_scores = matrix_scores[1:N]
        result_indices = [i[0] for i in matrix_scores]
        scores = [i[1] for i in matrix_scores]
        result = novels_df.iloc[result_indices,:].copy()
        
        result['score'] = scores
        return result

    def apply_filters(self, df):
        """Apply filters chosen by the user.

        Args:
            novels_df (DataFrame): _description_

        Returns:
            Series: Series object containing novels that contain the specified filters.
        """
        
        if st.session_state.genres and st.session_state.tags:
            df = df[df['genres'].apply(lambda genre : all(item in genre for item in st.session_state.genres))]
            df = df[df['tags'].apply(lambda tag : all(item in tag for item in st.session_state.tags))]
            items = df['novel_id']
        elif st.session_state.genres:
            df = df[df['genres'].apply(lambda genre : all(item in genre for item in st.session_state.genres))]
            items = df['novel_id']
        elif st.session_state.tags:
            df = df[df['tags'].apply(lambda tag : all(item in tag for item in st.session_state.tags))]
            items = df['novel_id']
        else:
            items=pd.Series() # TODO: Try not to use pd Series.
            
        return items

    def generate_mlb_matrix(self, novels_df):
        """MLB is good for limited categorical data, such as Genres.
        
        """
        
        mlb = MultiLabelBinarizer()
        return mlb.fit_transform(novels_df['genres'])# + novels_df['tags'])

    def generate_cv_matrix(self, novels_df):
        """CV is useful for the tags and author. 
        This will count each occurence of a word and convert it into a matrix.
        
        """
        
        count = CountVectorizer(stop_words='english')
        return count.fit_transform(novels_df['soup'])

    def _clean_synopsis(self, df):
        """
        Cleans a string of HTML tags, punctuation, line breaks and multiple whitespaces.
        
        Args:
            df : pandas DataFrame
            A pandas DataFrame containing a single string column with the synopsis text.
            
        Returns:
            synopsis (str): A cleaned string with no HTML tags, punctuation, line breaks, or multiple whitespaces. All characters are also converted to lowercase.
        """
        
        synopsis = ''.join(df)
        synopsis = re.sub(r'<.*?>', '', synopsis) # remove html tags
        synopsis = re.sub(r'[^\w\s]', '', synopsis) # remove punctuation and special characters
        synopsis = re.sub(r'\n', '', synopsis) # remove line breaks
        synopsis = re.sub(r'\s+', ' ', synopsis) # collapse multiple whitespaces into a single space
        return synopsis.lower() # convert to lowercase and split into words

    def generate_tfv_matrix(self, novels_df):
        """TD-IDF is the go-to-algorithm for analyzing raw text data. 
        It takes the inverse domain frequency and converts it into a matrix.
        
        """
        
        tfv = TfidfVectorizer(min_df=3, 
                            max_features=None,
                            strip_accents='unicode', analyzer='word', 
                            token_pattern=r'\w{1,}',
                            ngram_range=(1,3),
                            stop_words='english')

        novels_df['synopsis'] = novels_df['synopsis'].fillna('')
        novels_df['synopsis'] = novels_df['synopsis'].apply(self._clean_synopsis)
        return tfv.fit_transform(novels_df['synopsis'])

    def generate_numeric_data(self, novels_df):        
        """Lastly we have the numerical data, such as ratings, readers, 
        chapters, etc. Here we normalize and scale it so it fits in a 0-1 range.
        
        """
        
        ratings = novels_df['weighted_rating'].values
        chapters = novels_df['chapters'].values
        readers = novels_df['readers'].values
        favorites = novels_df['favorites'].values
        views = novels_df['total_views_all'].values
        
        #Remove outliers that negatively impact the cb-system.
        rb = RobustScaler()
        chapters = rb.fit_transform(chapters.reshape(-1, 1))
        readers = rb.fit_transform(readers.reshape(-1, 1))
        favorites = rb.fit_transform(favorites.reshape(-1, 1))
        views = rb.fit_transform(views.reshape(-1, 1))
        
        mm = MinMaxScaler(feature_range=(0,1))
        ratings = mm.fit_transform(ratings.reshape(-1, 1))
        chapters = mm.fit_transform(chapters)
        readers = mm.fit_transform(readers)
        favorites = mm.fit_transform(favorites)
        views = mm.fit_transform(views)
        
        
        return {"weighted_rating": ratings, 
                "chapters": chapters, 
                "readers": readers, 
                "favorites": favorites, 
                "views": views}

    @st.cache(show_spinner=False, persist=True, max_entries=5, ttl=3600)
    def fit(self, novels_df):
        """Fit the CBRecommender with the data provided

        """
        
        """Convert the tags, genres, fandom_tags into a list of strings."""
        
        features = ['tags', 'genres', 'fandom_tags']
        for feature in features:
            novels_df[feature] = novels_df[feature].apply(self.clean_data)

        novels_df['soup'] = novels_df.apply(self.create_soup, axis=1)
        
        mlb_matrix = self.generate_mlb_matrix(novels_df)
        cv_matrix = self.generate_cv_matrix(novels_df)
        tfv_matrix = self.generate_tfv_matrix(novels_df)
        numeric_data = self.generate_numeric_data(novels_df)

        # Stack the different matrixes from MLB, 
        # CV, TD-IDF, etc. into a collected 'feature_matrix'."""
        feature_matrix = hstack([mlb_matrix, cv_matrix, tfv_matrix, 
                                    numeric_data["weighted_rating"], numeric_data["chapters"], 
                                    numeric_data["readers"], numeric_data["favorites"], 
                                    numeric_data["views"]])

        # Calculate the cosine similarity between the different vectors 
        # in the feature_matrix. We use cosine_similarity because it is magnitude insensitive."""
        similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)
        
        indices = pd.Series(novels_df.index, index=novels_df['novel_id']).drop_duplicates()
        return similarity_matrix, indices