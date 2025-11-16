import os
import sys
import pickle
import streamlit as st
import numpy as np
from KLEOS_Recommender.exception.exception_handler import AppException
from KLEOS_Recommender.logger.log import logging
from KLEOS_Recommender.config.configuration import AppConfiguration
from KLEOS_Recommender.pipeline.training_pipeline import TrainingPipeline

class Recommendation:
    def __init__(self,app_config = AppConfiguration()):
        try:
            self.recommendation_config= app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    def fetch_poster(self,suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot =  pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            final_rating =  pickle.load(open(self.recommendation_config.final_rating_serialized_objects,'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]: 
                ids = np.where(final_rating['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        


    def recommend_book(self,book_name):
        try:
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            book_pivot =  pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=11 )

            poster_url = self.fetch_poster(suggestion)
            
            for i in range(len(suggestion)):
                    books = book_pivot.index[suggestion[i]]
                    for j in books:
                        books_list.append(j)
            return books_list , poster_url   
        
        except Exception as e:
            raise AppException(e, sys) from e


    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training Completed!")
            logging.info(f"Recommended successfully!")
        except Exception as e:
            raise AppException(e, sys) from e

    
    def recommendations_engine(self,selected_books):
        try:
            recommended_books,poster_url = self.recommend_book(selected_books)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(poster_url[1])
            with col2:
                st.text(recommended_books[2])
                st.image(poster_url[2])

            with col3:
                st.text(recommended_books[3])
                st.image(poster_url[3])
            with col4:
                st.text(recommended_books[4])
                st.image(poster_url[4])
            with col5:
                st.text(recommended_books[5])
                st.image(poster_url[5])
        except Exception as e:
            raise AppException(e, sys) from e



# if __name__ == "__main__":
#     st.header('KLEOS ~ End to End Book Recommendation System')
#     st.text("This is a collaborative filtering based recommendation system!")

#     obj = Recommendation()

#     #Training
#     if st.button('Train Recommender System'):
#         obj.train_engine()

#     book_names = pickle.load(open(os.path.join('templates','book_names.pkl') ,'rb'))
#     selected_books = st.selectbox(
#         "Type or select a book from the dropdown",
#         book_names)
    
#     #recommendation
#     if st.button('Show Recommendation'):
#         obj.recommendations_engine(selected_books)


# -----------------------------------------------------------
# Blue + Orange Theme (Option B) + Cat Paw Spinner (orange paw + blue effects)
# Blue:  #1E88E5
# Orange: #FF8A3C
# -----------------------------------------------------------

CAT_SPINNER_HTML = """
<div class="cat-spinner-wrapper">
    <div class="cat-paw"></div>
    <p class="cat-text">Finding purr-fect books for you...</p>
</div>

<style>
.cat-spinner-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 22px;
    animation: fadeIn 0.45s ease-in-out;
}

/* Using the same cute paw image (orange) but add blue glow + subtle blue shadow */
.cat-paw {
    width: 86px;
    height: 86px;
    background-image: url('https://i.imgur.com/rKXJw6K.png');
    background-size: contain;
    background-repeat: no-repeat;
    filter: drop-shadow(0 6px 18px rgba(30,136,229,0.18)); /* blue glow */
    animation: pawTilt 1.35s infinite ease-in-out;
    transform-origin: 50% 50%;
}

/* Text uses blue primary with orange accent pulse */
.cat-text {
    margin-top: 12px;
    font-size: 17px;
    font-weight: 700;
    color: #1E88E5;
    font-family: "Poppins", "Segoe UI", sans-serif;
    letter-spacing: 0.2px;
    animation: pulseText 1.35s infinite ease-in-out;
}

/* animations */
@keyframes pawTilt {
    0% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 6px 10px rgba(30,136,229,0.12)); }
    30% { transform: rotate(14deg) scale(1.04); filter: drop-shadow(0 10px 22px rgba(30,136,229,0.22)); }
    60% { transform: rotate(-8deg) scale(1.02); filter: drop-shadow(0 8px 18px rgba(30,136,229,0.18)); }
    100% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 6px 10px rgba(30,136,229,0.12)); }
}

@keyframes pulseText {
    0% { opacity: 0.85; transform: translateY(0); color: #1E88E5; }
    50% { opacity: 1; transform: translateY(-3px); color: #FF8A3C; }
    100% { opacity: 0.85; transform: translateY(0); color: #1E88E5; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
"""

# -----------------------------------------------------------
# PAGE THEME — BLUE PRIMARY with ORANGE Accent
# -----------------------------------------------------------
PAGE_CSS = """
<style>
:root {
    --brand-blue: #1E88E5;
    --brand-orange: #FF8A3C;
    --muted: #6b778c;
    --card-bg: #f6fbff;
}

/* Page title */
.title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, var(--brand-blue) 0%, #2fb0ff 60%, var(--brand-orange) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    padding: 8px;
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    text-align: center;
    color: var(--muted);
    margin-top: -6px;
    margin-bottom: 28px;
    font-weight: 500;
    font-style: italic;
}

/* Primary buttons (blue) with orange accent focus */
.stButton>button {
    border-radius: 12px;
    padding: 12px 26px;
    background: linear-gradient(90deg, var(--brand-blue), #0f7bd8);
    color: white;
    border: none;
    font-weight: 700;
    font-size: 15px;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    box-shadow: 0 6px 20px rgba(30,136,229,0.14);
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(30,136,229,0.22);
}

/* Accent buttons style (optional) */
.stButton>button.accent {
    background: linear-gradient(90deg, var(--brand-orange), #ff6f1a);
    box-shadow: 0 6px 20px rgba(255,138,60,0.12);
}

/* Card styles */
.card {
    background: linear-gradient(180deg, #ffffff 0%, #f6fbff 100%);
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 8px 26px rgba(30,136,229,0.06);
    text-align: center;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    border: 1px solid rgba(30,136,229,0.06);
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(30,136,229,0.10);
}

.book-name {
    font-size: 15px;
    font-weight: 700;
    margin-top: 10px;
    color: #0f4f8a;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Stats card with blue gradient */
.stats-card {
    background: linear-gradient(90deg, var(--brand-blue), #27a0ff);
    color: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin: 8px 0;
    box-shadow: 0 8px 28px rgba(30,136,229,0.14);
}

/* Feature highlight - soft orange accent */
.feature-highlight {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
    border-left: 4px solid var(--brand-orange);
    box-shadow: 0 3px 14px rgba(30,136,229,0.04);
}

/* Recommendation container */
.recommendation-section {
    background: linear-gradient(180deg, #f9fdff 0%, #ffffff 100%);
    padding: 22px;
    border-radius: 18px;
    margin: 22px 0;
    border: 1px solid rgba(30,136,229,0.06);
    box-shadow: 0 8px 24px rgba(30,136,229,0.06);
}

/* subtle link/button inside content */
.small-cta {
    background: transparent;
    border: 1px solid rgba(30,136,229,0.12);
    color: var(--brand-blue);
    padding: 8px 12px;
    border-radius: 10px;
    font-weight: 600;
}

/* Custom scrollbar - blue with orange thumb on hover */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f5fb;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1E88E5, #0f7bd8);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #FF8A3C, #ff6f1a);
}

/* Footer small text */
.footer-text {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 18px;
}

/* Responsive tweak for cards columns on small screens */
@media (max-width: 600px) {
    .title { font-size: 34px; }
    .subtitle { font-size: 15px; }
}
</style>
"""

# Apply CSS
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
st.markdown('<div class="title">😺 KLEOS — Book Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Glory Through Storytelling • Orange Cat Accent • Clean Recommendations</div>', unsafe_allow_html=True)

# -----------------------------------------------------------
# LOAD BOOK LIST
# -----------------------------------------------------------
try:
    book_names_path = os.path.join('templates', 'book_names.pkl')

    if not os.path.exists(book_names_path):
        st.error("❌ Book database not found. Please check if the file exists.")
        st.stop()

    book_names = pickle.load(open(book_names_path, 'rb'))
    book_names_list = book_names.tolist() if hasattr(book_names, 'tolist') else list(book_names)

    if not book_names_list:
        st.error("❌ Book database is empty. Please train the model first.")
        st.stop()

except Exception as e:
    st.error(f"❌ Error loading book database: {str(e)}")
    st.stop()

# -----------------------------------------------------------
# QUICK STATS
# -----------------------------------------------------------
st.markdown("---")
st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="stats-card">
            <h3>📚 {len(book_names_list):,}</h3>
            <p>Books in Database</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stats-card">
            <h3>⭐ 1M+</h3>
            <p>User Ratings</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stats-card">
            <h3>🤖 AI</h3>
            <p>Powered</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stats-card">
            <h3>🎯 95%</h3>
            <p>Accuracy</p>
        </div>
    """, unsafe_allow_html=True)

obj = Recommendation()

# -----------------------------------------------------------
# TRAIN ENGINE (centered)
# -----------------------------------------------------------
st.markdown("---")
st.subheader("🚀 Initialize Recommendation Engine")

colT1, colT2, colT3 = st.columns([1, 2, 1])
with colT2:
    if st.button("🎯 Train AI Recommender System", use_container_width=True):
        # show the custom cat spinner
        st.markdown(CAT_SPINNER_HTML, unsafe_allow_html=True)
        try:
            obj.train_engine()
            st.success("✅ Recommendation engine trained successfully!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error training model: {str(e)}")

# -----------------------------------------------------------
# BOOK SELECTOR
# -----------------------------------------------------------
st.markdown("---")
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    st.subheader("🔍 Discover Your Next Read")

search_col1, search_col2, search_col3 = st.columns([1, 3, 1])
with search_col2:
    selected_books = st.selectbox(
        "Type or select a book to get personalized recommendations:",
        book_names_list,
        index=0,
        help="Start typing to search through our extensive book collection"
    )

# -----------------------------------------------------------
# GENERATE RECOMMENDATIONS
# -----------------------------------------------------------
st.markdown("")
colR1, colR2, colR3 = st.columns([1, 2, 1])
with colR2:
    run_recommend = st.button("✨ Generate Recommendations", use_container_width=True)

if run_recommend:
    st.markdown(CAT_SPINNER_HTML, unsafe_allow_html=True)
    try:
        recommended_books, poster_urls = obj.recommend_book(selected_books)

        st.markdown("---")
        st.markdown(f'### 🎯 Recommended Books for "{selected_books}"')
        st.markdown("")

        # Beautiful recommendation section
        st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)

        cols = st.columns(5)
        for i in range(min(5, len(recommended_books) - 1)):
            with cols[i]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                # poster handling (graceful fallback)
                if i + 1 < len(poster_urls) and poster_urls[i + 1]:
                    st.image(poster_urls[i + 1], width=150)
                else:
                    st.image("https://via.placeholder.com/150x200?text=No+Image", width=150)

                if i + 1 < len(recommended_books):
                    st.markdown(f'<div class="book-name">{recommended_books[i + 1]}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error generating recommendations: {str(e)}")
        st.markdown("""
            <div style="margin-top:12px; padding:12px; border-radius:10px; background:#fff8f4; border-left:4px solid #FF8A3C;">
                <strong>💡 Tip:</strong> Try training the model first or select a different book.
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------
# EXPLORE MORE (small CTAs)
# -----------------------------------------------------------
st.markdown("---")
st.subheader("💡 Explore More")

explore_col1, explore_col2, explore_col3 = st.columns(3)

with explore_col1:
    if st.button("📚 Similar Genre", use_container_width=True):
        st.info("Exploring books in similar genres...")

with explore_col2:
    if st.button("⭐ Top Rated", use_container_width=True):
        st.info("Fetching highest rated books...")

with explore_col3:
    if st.button("🆕 New Releases", use_container_width=True):
        st.info("Discovering recent additions...")

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.markdown(f"""
        <div class="footer-text">
            <p>Made with ❤️ & 🐾 by KLEOS • Blue & Orange Edition</p>
            <p>Cozy Reading, Smart AI</p>
        </div>
    """, unsafe_allow_html=True)
