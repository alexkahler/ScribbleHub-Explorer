"""
FAQ and About page (Duh!).
"""
from streamlit_extras.stoggle import stoggle
import streamlit as st

from tools import utility
from tools.constants import Pages
from assets import page_elements

def main():
        
    st.title("What's with this app?")

    st.markdown("### aka. the FAQ and about page")
    st.markdown('___')
    st.markdown("""
*Update - 19-02-2023: I'm brainstorming ways to get the necessary data without accessing SH servers. Stay tuned for updates on [SH Forums](https://forum.scribblehub.com/threads/scribblehub-explorer-%E2%80%93-an-ai-powered-novel-recommendation-engine-feedback-needed.13028/)  
Update - 16-02-2023: Tony has asked me to stop scraping SH, so I will not be able to update the ScribbleHub Explorer
unless something changes in the future. I don't know if I will keep adding features, just because it's a good way to train my programming skills.
But this will not include updated content (novels and users). The dataset used in this app is from around last week of January 2023, and the novels are from the beginning of 
Februray 2023. The reading lists had some issues due to the way it was collected, and as such, not all users are 
part of the initial load. If you aren't one of them. Then, sorry. Tough luck.  
I do appreciate you stopping by, and I wish you luck in finding your next novel to read.  
/Unknown Novelist*
                
Welcome to **ScribbleHub Explorer**, your one-stop-shop for finding your next web-novel (or so I hope)!  
As an avid reader, have you ever found yourself in a nightmare where you can't seem to find any good stories?
Well, Unknown Novelist (that's me!) has been there too. That's why I created this project, to help readers 
like you and me find the next great novel to sink our teeth into.

**ScribbleHub Explorer** was created with three key goals in mind: to help aspiring authors get more readers who
love their stories, to enable readers find a good story that suits their taste, and to help 
[ScribbleHub](https://www.scribblehub.com/) generate more traffic.  
As you may know, I'm strongly against Webnovel and their monetization scheme. I believe that authors deserve to
be paid for their hard work and effort, but I don't think a paywall is the right solution for the webnovel 
community. So, I came up with a way to give back to the community and help keep ScribbleHub the free platform 
that it is.

So, what is **ScribbleHub Explorer**? It's a recommendation system with two parts. The first part is a "pure" 
*Content-based Recommendation System* that calculates the Cosine Similarity between the input and all other 
novels found on ScribbleHub. This system uses existing "features" such as the novel's synopsis, genres, tags,
fandom, rating, etc. to generate recommendations. While these recommendations are not personalized, they can
still be pretty good if you spend a little effort selecting filters, etc.

The second recommendation engine is an AI/ML (Artificial Intelligence/Machine Learning) system that uses an
*"User-Item based Implicit Collaborative Filtering"* approach and *Alternating Least Squares Matrix 
Factorization* to calculate recommendations (yea, that's a mouthful - and I wanted to sound smart).  
In layman's terms, it compares what you have in your library with what others have and finds what you might
be missing. This method generally gives good suggestions, but it's subject to the "cold start problem" which
means that if you don't have any novels or very few novels in your reading list, the AI can't generate any
recommendations for you. I have some ideas for improving this using a hybrid-engine which you can find out
more about in the [future updates](#future-updates) section below.

But that's just the tip of the iceberg! There are two supporting projects that make **ScribbleHub Explorer**
possible. The first is the **ScribbleHub Spiders**, the workhorse behind gathering all the necessary data.
The Spiders crawl through all 23,000+ novels and save the main-page statistics and 120,000+ users. It's 
important to note that I do NOT collect any copyrighted material or personal information, such as chapter 
content or user details like location. The Spiders only collect the minimum required information according to 
ethical scraping guidelines such as the title, synopsis, rating, readers, favorites, and number of chapters.
All links go directly to the novel and I don't host any content. If you're an author and you would like your 
novel removed from the app, just contact me using the [contact form](#contact).

The **ScribbleHub Spiders** will index **ScribbleHub** once a month, meaning the app will only be updated once
a month with new novels. If you're a user and your profile is disabled for public viewing or you just
created a profile on ScribbleHub, check back later as I plan to make a feature to passively request user profiles soon.
Sorry, but there's no other way around this unless Tony (ScribbleHub admin) 
gives me direct access to the database.

After the Spiders have finished crawling, they generate datasets used by **ScribbleHub RecSys** to train the AI
in recommending novels. This is a computer-intensive task that takes about 2-3 days of compute time, but it 
results in the AI being pre-trained and reduces load time for the end-user (that's you!). The datasets are available on GitHub
as a JSONL file, as well as the source code for both the Spiders and RecSys.
 
Finally, the Statistics page offers information on trending genres, tags, and other data that can inform authors
in their writing and readers in their discovery. I also have plans to update the Statistics page to generate
personalized statistics for readers.    

To end, I would like to thank you for using this app. If you should have any suggestions for improvements then
don't hesitate to contact me using the [contact form](#contact) below. I have several [updates planned](#future-updates), 
so hang tight and check back often. If you want to show your support, then I would greatly appreciate any donations using [Ko-Fi](https://ko-fi.com/B0B2756JF).  
Buy me a coffe :coffee: so I can code harder! :)

Sign off,  
/Unknown Novelist.""")
    
    st.markdown("___")
    st.markdown("""### ❤️ Special Thanks:
Special shoutout to those who have made this app possible.
- [Tony](https://forum.scribblehub.com/members/tony.11/) :muscle:
- [ChatGPT](https://chat.openai.com/) 🤖
                """)
    
    st.markdown("___")
    st.markdown(f"""### ❓ FAQ:""")
    stoggle("How does ScribbleHub Explorer work?", 
            """ScribbleHub Explorer consists of three components: the recommendation system (ScribbleHub Explorer), 
the ScribbleHub RecSys and the ScribbleHub Spiders. The recommendation system uses two different engines to 
provide readers with personalized recommendations: a content-based recommendation system and an AI/ML system. 
Finally, there the several add-ons, such as the statistics page which provides valuable insights for both 
readers and authors. """)
    stoggle("What is the content-based recommendation system?",
            """The content-based recommendation system calculates the cosine similarity between the input and 
            all other novels on ScribbleHub, using existing features such as synopsis, genres, tags, fandom, and 
            rating.""")
    stoggle("What is the AI/ML system?",
            """The AI/ML system is a "User-Item based Implicit Collaborative Filtering" using Alternating Least 
            Squares (ALS) Matrix Factorization to make personalized recommendations based on the reader's 
            preferences and reading history.""")
    stoggle("How is the data collected?",
            """The data used by ScribbleHub Explorer is collected by the ScribbleHub Spiders, which are developed
            on the backbone of Scrapy. The Spiders crawl through over 23,000 novels and collect the minimum 
            required information, but do not collect any copyrighted material or personal information.""")
    stoggle("How often is the data updated?",
            """For novels: I aim to update the dataset used by ScribbleHub Explorer once a month. For users I plan
            to create a feature which can passively ScribbleHub open user request in order to avoid overloading
            their servers with traffic.""")
    stoggle("What if my profile is disabled for public viewing or I've just created a new profile?",
            """If your profile is disabled for public viewing or you've just created a new profile, it may not be 
            immediately reflected in ScribbleHub Explorer until I have created the change to query ScribbleHub
            for the latest user profile.""")
    stoggle("What if I want my novel to be removed from ScribbleHub Explorer?",
            """If you want your novel removed from this app, please contact me using the contact form below.""")
    stoggle("What if I want my user profile to be removed from ScribbleHub Explorer?",
            """If you want your user profile to be removed, please contact me using the contact form below.""")
    stoggle("Is ScribbleHub Explorer affiliated with ScribbleHub?",
            """No, ScribbleHub Explorer is not affiliated with ScribbleHub in any way. It's a personal project 
            created by me ("Unknown Novelist") with the goal of helping readers discover new novels and helping
            authors get more exposure for their work.""")
    stoggle("Why can't I find my favorite novel on ScribbleHub Explorer?",
            """There might be several reasons why you might not be able to find your favorite novel on 
            ScribbleHub Explorer. First, ScribbleHub Spiders only index novels that are publicly available on 
            ScribbleHub. Next, if your favorite novel has less than 5 chapters, it won't be included in the app. 
            Third, ScribbleHub Spiders only index a novel once a month, so if your favorite novel was recently
            added to ScribbleHub, it might not be included in the app yet. Finally, if your favorite novel was 
            removed from ScribbleHub, it won't be included in the app.""")
    stoggle("Why don't my recommendations match my reading list?",
            """If your recommendations don't match your reading list, there could be several reasons. 
            First, if you haven't added any novels to your reading list, the AI won't have any information to 
            generate recommendations. Second, the AI is based on a concept called "User-Item based Implicit 
            Collaborative Filtering," which means that it cross-references your reading list with other users' 
            reading lists. If your reading list is unique and doesn't match with other users' reading lists, the 
            AI might not generate accurate recommendations.""")
    stoggle("Can I help improve the recommendations?",
            """Yes, you can help improve the recommendations by adding more novels to your reading list and by 
            rating the novels that you like! This will help the AI learn what you like and generate more accurate 
            recommendations.""")
    stoggle("What's with the anime girl in the sidebar?",
            """Ah, yes. I see you've met NUF-chan (https://forum.novelupdates.com/members/nuf-mascot.52471/). 
            She's apparently NovelUpdates' (a sister site to ScribbleHub) mascot.""")
    stoggle("Will you host my artwork in the sidebar?",
            """Yes! Please format your picture to a 150x150 pixel size and contact me using the 
            contact form below.""")
    stoggle("""I have a public reading list, but why does it say that "user hasn't been crawled?""",
            """There can be several reason behind this. Most likely it's because your reading list has less than 
            5 novels. Other reasons could be that you've only recently made it public and that the Spiders have 
            missed your profile. It's also possible that the Spider had a meltdown over your profile and decided 
            to skip it entirely (that can happen). Please contact me if believe that this is a consistent bug.""")
    stoggle("""What's "Weighted Rating" and how does it differ from ScribbleHub's normal rating?""",
                """One of the key-issues with a regular rating/voting system is that any novel or item that has 
                been rated 5 by one user, will jump straight to the top of a ranking list. Moreover, as more users 
                vote, items that have few votes generally have higher ranking due to the nature of how humans vote
                (either 1 or 5). Lastly, such ranking lists do not take popularity of an item into account. 
                To combat this, IMDB made a simple, but very effective math calculation to factor in popularity, 
                average rating, and number of votes. This is the same algorithm that sits behind IMDB's Top 250 
                Movies. The equation is like this:  \n
$${(WR) = \dfrac{v}{(v+m)} \\times R + \dfrac{m}{(v+m)} \\times C}.$$  
Where;  
- *R* = average for the movie (mean) = (Rating)  
- *v* = number of votes for the movie = (votes)  
- *m* = minimum votes required to be listed in the Top 250 (currently 25000)  
- *C* = the mean vote across the whole report (currently 7.0)

The advantage of using this equation to calculate the ratings is that it takes the average rating 
across all items into account, and the number of votes casts including the minimum number to be 
considered (ScribbleHub Explorer has this set to the 90th percentile). With this, novels with only 
one 5* star rating will not have the same impact, or *weight* as a popular novel with many votes, 
but not as high an average rating.
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>""")
    stoggle("Is your Top 100 list specially curated by you?",
            """See my answer above.""")
    stoggle("""Why does the CB Engine and CF Engine's "Similar Items" give me different recommendations?""",
            """Short answer: They're different. Slightly longer answer: The reason that they generate different recommendations
            is due the different way that they work. The Content-Based Engine only uses the novel's meta-information
            such as synopsis, genres, tags, and ratings to compare all other novels on ScribbleHub and then calculate
            a ranking list on what is most similar to what you gave it. The Collaborative Filtering Engine is more
            advanced. It uses a complex AI technique to figure out what you like, and then compares your reading list
            with everyone else's to understand what you might be missing out on. In short, it doesn't actually use any
            of the meta-data that each novel has, but "merely" by understanding what everyone else is reading, it can
            come up with a similar novel recommendation based on that. This is why the two systems might give completely
            different recommendations.""")
    stoggle("""What can I do as an author to improve my ranking in the Content-Based Recommendations?""",
            """There are several things that you can do as an author to help improve your ranking visibility.  
            Here are the key takeaways:
            1. Ensure that your novel's synopsis has a clear description of your story.  
            Much like how a human reads your synopsis, so too does the Content Based Engine. It compares the words 
            in other novel's synopsis with yours, which means if it is too unique (i.e., has a lot of links), then 
            it's likely you would be ranked lower. This doesn't mean that you should make your synopsis completely 
            generic either, as that would just put, you in the herd together with the rest. Instead, you should ask 
            yourself, why should other people read my story solely based on my synopsis? And try to write the answer 
            to that question in the form of a synopsis.
            2. Update your genres and tags.  
            The Content-Based Engine uses tags and genres to also make an "informed" decision about whether to recommend 
            your story or not to the user. It examines what the user has requested to find are similar, and then calculates
            the similarity between what is in your novel to what the user has given as input. In short, this means that you
            should try to have the genres and tags that best represent your story. Genres have a slightly higher weight 
            than tags, but that doesn't mean that tags are ignored. If genres describe the *theme* of your story, then tags
            would describe what *going on* in your story. Again, try to hit a middle point where you don't just have 1 genre 
            to describe your story, but instead, ask yourself, "what are the common elements between what I have written, 
            and how do I slightly stand out from the crowd?"
            3. Get more ratings, reviews and favorites.  
            The Content-Based Engine also uses metrics such as number of revies, favorites, and ratings to make a decision 
            about how popular your novel is. If you're a new author with a newly published story; worry not! This is merely 
            an aspect and cannot outweigh the 2 previous features that I mentioned. It uses these metrics as a means to 
            judge whether the user is looking for a popular novel, or if they're trying to find something new. So, as the 
            popularity of your novels grow, you can expect that the novels that you are ranked together with also changes. 
            Don't be afraid to ask your readers for a rating and review!""")
    
    st.markdown("___")
    st.markdown("""### 🦟 Known Bugs:
- When selecting genres or tags from the sidebar, the dropdown will close after each choice.  
- When typing the genres or tags, you will need to re-select the multi-select after each choice.
- When clicking "More>>" some expand boxes can "jump" before contents fill the empty space.
- Sometimes the input box will not respond when entering a novel ID or URL. Refreshing the page will usually help.
- There's some weird behaviour going on in the Top 100 list when you combine filters and the number to show.
- When selecting a filter (Genre or Tag) and navigating to the Stats or About page, and back to a page where filters are enabled, you will not be able to remove the filters without first removing them re-adding them again.
- Generally, any bug can be fixed by refreshing the page. If this doesn't work for you, please contact me.  
  
Please be patient as I work to fix these bugs. In the mean time, here's a button that you can smash to take out your frustrations.""")
    st.button('Button', on_click=button_counter)
    
    st.markdown("___")
    st.markdown("""### 📋 Changelog:
- Ver. 0.1b: Inital beta - expect bugs and crashes. Please submit a bug-report if something happens. You can find a contact form below.""")
    
    st.markdown("___")
    st.markdown("""### 🚧 Future Updates:
- ⚙️ Dynamically update recommendation engine based on new users and novels. E.g., if a user has enabled public viewing of their reading-list, or changed their reading list, then query ScribbleHub for the latest version.
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
- ⚡ Migrate Dataset to online Database like MySQL, PostGRES, etc.""")
    
    st.markdown("___")
    st.markdown(""" ### 🔮 Far Future Updates:
- 🕹️ Implement "Load More" button for more novels beyond the user-defined limit of 25 in recommendations.
- 📡 Index NovelUpdates to generate recommended novels outside of ScribbleHub. *"Will this stil be called 'ScribbleHub' Explorer by then?"*
- 🏡 Migrate to a better server or host own website.""")
    
    st.markdown("___")
    st.markdown("""### 💌 Contact:""")
    st.markdown(f"""<form action="https://formsubmit.co/e24e26f25ffc925223bb73f52292d71b" method="POST">
                        <select type="_subject" name="_subject">
                            <option value="General Query">General Query</option>
                            <option value="Bug Report">Bug Report</option>
                            <option value="Feedback/Suggestions">Feedback/Suggestions</option>
                            <option value="Art Submission">Art Submission</option>
                            <option value="Profile Takedown Request">Profile Takedown Request</option>
                            <option value="Novel Takedown Request">Novel Takedown Request</option>
                            <option value="Other">Other</option>
                        </select>
                        <input type="text" name="name" placeholder="Your name" required>
                        <input type="email" name="email" placeholder="Your email" required>
                        <textarea name="message" placeholder="Your message" required></textarea>
                        <input type="hidden" name="_autoresponse" value="Thank you for your message. I'll get back to you as soon as possible.">
                        <button kind="secondaryFormSubmit" class="css-nkvcxn" type="submit" value="Send">Send</button>
                </form>""", unsafe_allow_html=True)
    
    st.markdown("""
                <style>
                /* Style inputs with type="text", select elements and textareas */
                input[type=text], input[type=email], select, textarea {
                width: 100%; /* Full width */
                padding: 12px; /* Some padding */ 
                border: 1px solid; /* Gray border */
                border-radius: 4px; /* Rounded borders */
                box-sizing: border-box; /* Make sure that padding and width stays in place */
                margin-top: 6px; /* Add a top margin */
                margin-bottom: 16px; /* Bottom margin */
                background-color: #1c2126;
                border-bottom-color: rgb(38, 39, 48);
                border-top-color: rgb(38, 39, 48);
                border-left-color: rgb(38, 39, 48);
                border-right-color: rgb(38, 39, 48);
                color: rgb(232, 232, 232);
                transition-timing-function: cubic-bezier(0.2, 0.8, 0.4, 1);
                transition-property: border, box-shadow, background-color;
                resize: vertical /* Allow the user to vertically resize the textarea (not horizontally) */
                }             
                form {
                    padding: calc(1em - 1px);
                    border: 1px solid;
                    border-radius: 0.25rem;
                    border-color: rgba(232, 232, 232, 0.2);
                }
                </style>""", unsafe_allow_html=True)


def button_counter():
    if 'button_counter' not in st.session_state:
        st.session_state['button_counter'] = 0
    else:
        st.session_state['button_counter'] += 1
    if st.session_state.button_counter == 100:
        st.balloons()

if __name__ == '__main__':
    st.set_page_config(
        page_title=Pages.Page_4.value.get('page_name'),
        page_icon=Pages.Page_4.value.get('icon'),
        layout='centered',
        initial_sidebar_state='collapsed'
    )
    utility.init_sessions_state()
    page_elements.sidebar_menu(Pages.Page_4)  
    main()
    page_elements.support_button()
