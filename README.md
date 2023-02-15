# ScribbleHub Explorer
ScribbleHub Explorer is a project aimed at providing AI powered recommendations for users of ScribbleHub. It does so by using two recommendation systems - a Content-Based Recommendation System based on Cosine Similarity and a User-Item Collaborative Filtering Recommendation System using Alternating Least Squares (Matrix Factorization). The dataset used for these recommendations is generated from implicit feedback scraped from ScribbleHub reading lists.

The project includes a Top 100 page which uses IMDB's Top 250 ranking system, a statistics page and several other pages.

Note that this is still in early stages of development, so expect bugs and crashes. I'm working on getting them fixed. If you should experience any unexpected crashes, or have general feedback or suggestion, please contact me.

## Features
Two methods of generating recommendations - Content-Based and Collaborative Filtering  
A Top 100 page that uses IMDB's Top 250 ranking system  
A statistics page with the latest scraped novel statistics  
The ability to filter viewed novels on pages 1, 2, and 3 using the filter options in the sidebar  
Ability to sort novels on various of measures, such as Popularity, Favorites, Readers, Chapters, etc.  

## Requirements
To run ScribbleHub Explorer, you will need the following dependencies installed:

    - streamlit==1.18.1
    - scipy==1.10.0
    - pandas==1.5.3
    - numpy==1.24.1
    - zstandard==0.19.0
    - scikit-learn==1.2.1
    - implicit==0.6.2
    - streamlit-extras==0.2.6

## Pages
ScribbleHub Explorer has five main pages:

Page 1 is for "pure" Content-Based Recommendations. Users can input the ID for a novel that they want recommendations for.
![Main page for Content-Based Recommendations](https://i.imgur.com/Xee1sSc.jpeg)

Page 2 is for Collaborative Filtering Recommendations. Users can type in their user ID in the sidebar to view recommendations based on their reading lists. 
![Page 2](https://i.imgur.com/a8JPpur.jpeg)

In the second tab, users can input the ID for a novel and view similar novels based on the input.
![Similar novels tag](https://i.imgur.com/TuvxHNb.jpeg)

Page 3 is the Top 100 page.
![Top 100](https://i.imgur.com/W72DAWj.jpeg)

Users can filter any viewed novels using the filter options in the sidebar on pages 1, 2, and 3.
![Filtering recommendations](https://i.imgur.com/Gv7qWiz.jpeg)

Page 4 is the statistics page, where the latest scraped novel statistics can be found.
![Statistics](https://i.imgur.com/hs4XRrK.jpeg)

Page 5 is the FAQ & About page.


## Future Updates
The following updates are planned for ScribbleHub Explorer:

- ⚙️ Dynamically update recommendation engine based on new users and novels. E.g., if a user has enabled public viewing of their reading-list, or changed their reading list, then query ScribbleHub for the latest version. This is both to reduce the load on ScribbleHub servers, but also to improve the user experience (alway having the latest updated reading list).
- 🧹 (Back end) Do some general housekeeping and refactor spaghetti code.
- 🏋️ Reduce load time by reducing heavy dataset and loading novel data directly from ScribbleHub. This will also reflect real-time changes done to the novels.
- 📈 Get personalized stats in the Statistics page (Stats Gore) and see how you compare to other readers in your reading hobby.
- 🗺️ Show the novel or user info, which the recommendations are based on, after input.
- 🔘 Ability to select AND / OR option with filters. Currently it is set to "AND".
- 📈 More sorting options (sort by chapters per week, word count, pageviews, date added, number of ratings, reviews, etc.)
- 🩸 MOAR filtering options (Fandom, Content Warning, Story Status)
- ⛔ Ability to select whether the filter should exclude or include the choices.
- ✔️ Show on the recommendation list, whether a user has already seen a novel.
- 💅 Beautify the app. Right now the novel list looks the Ugly Bastard you always feared from Otome Dori. (Remove default blue color links, add nice looking badges for tags and genres, etc.)
- 🆔 Input user ID or username to view personalized ScribbleHub reading stats.
- 🔖 (Back end) Dynamically load tags from crawled novels. Right now it's hard coded, so if there's an unknown tag out there, then it won't show up.
- 📑 Use Fuzzy Match logic to detect "dropped" reading lists. Yes. Some people have their primary reading lists as their dropped novels.
- 💡 Transition to LightFM CF Engine with WARP algorithm for CF-Recommendations. ALS (Alternating Least Squares) is good, but a hybrid-recommender engine would allow for some interesting recommendations as that could consider not just what other users have added to their reading list, but also "meta" data, like genres, synopsis, etc.
- ☀️ Light and Dark mode
- ⚡ Migrate Dataset to online Database like MySQL, PostGRES, etc.

## How To Run
To run the project, install the dependencies, and use the Streamlit command ´streamlit run Recommend_Me_Stuff.py´

## Contributing
If you are interested in contributing to the ScribbleHub Explorer project, please send me a message. Do not make pull requests to the active main branch. You are free to fork the project as you like.

## Extra
ScribbleHub Explorer is one part of three. I suggest you also check out:
- [ScribbleHub RecSys](https://github.com/alexkahler/scribbleHub-recsys): The main part which trains the AI and outputs the models used in ScribbleHub Explorer. 
- [ScribbleHub Spider](https://github.com/alexkahler/scribbleHub-spider): A Scrapy based web-crawler. It is the "workhorse" behind gathering the necessary data for creating recommendation.