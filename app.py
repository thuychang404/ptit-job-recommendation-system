import streamlit as st
import pandas as pd
import os

# Load data
df = pd.read_pickle('df_html.pkl')
similarity = pd.read_pickle('similarity.pkl')

# st.write("DataFrame Columns:", df.columns)

# Placeholder for user authentication
def login_frm():
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username == '1' and password == '2':
            st.session_state['authenticated'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

def recommendation(title, country, num_recommendations=10):
    try:
        idx = df[(df['Title'] == title) & (df['Country'] == country)].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:num_recommendations]
        
        recommended_jobs = [df.iloc[i[0]] for i in distances]
        return recommended_jobs
    except IndexError:
        return []

def job_details_frm(index):
    job = df.iloc[index]
    st.write(f"## {job['Title']}")
    st.write(f"### Description:")
    st.markdown(f"{job['Description'].replace('\r', '').replace('\n\n\n', ' ')}", unsafe_allow_html=True)
    st.write(f"### Requirements:")
    st.markdown(f"{job['Requirements'].replace('\r', '').replace('\n\n\n', ' ')}", unsafe_allow_html=True)
    st.write(f"### Location: {job['City']}, {job['State']}, {job['Country']}")
    if st.button('Back to recommendations'):
        st.session_state['view'] = 'home'

def save_favorite_job(job):
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    st.session_state['favorites'].append(job)
    st.success("Job saved to favorites!")

def view_favorites_frm():
    st.write("## Favorite Jobs")
    if 'favorites' in st.session_state and st.session_state['favorites']:
        for idx, job in enumerate(st.session_state['favorites']):
            st.write(f"## {idx+1}. {job['Title']}")
            st.write(f"### Description:")
            st.markdown(f"{job['Description'].replace('\r', '')}", unsafe_allow_html=True)
            st.write(f"### Requirements:")
            st.markdown(f"{job['Requirements'].replace('\r', '')}", unsafe_allow_html=True)
            st.write(f"### Location: {job['City']}, {job['State']}, {job['Country']}")
        if st.button('Back to recommendations'):
            st.session_state['view'] = 'home'
    else:
        st.write("No favorite jobs saved.")
        if st.button('Back to recommendations'):
            st.session_state['view'] = 'home'

def send_email(job):
    # Dummy function to simulate email sending
    st.success(f"Job details sent to your email: {job['Title']}")

def export_recommendations(jobs):
    recommendations_df = pd.DataFrame(jobs)
    st.download_button(label="Download Recommendations", data=recommendations_df.to_csv().encode('utf-8'), file_name='recommendations.csv', mime='text/csv')

def toggle_theme():
    if st.session_state['theme'] == 'light':
        st.session_state['theme'] = 'dark'
    else:
        st.session_state['theme'] = 'light'

def setup_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'
    if 'view' not in st.session_state:
        st.session_state['view'] = 'home'
    if 'view_favorites' not in st.session_state:
        st.session_state['view_favorites'] = False
        
def side_bar():
    # Logo
    logo_path = 'logo.jpg'
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path,use_column_width=1,caption="Bridge Jobs - CẦU NỐI ĐẾN TƯƠNG LAI")
    else:
        st.sidebar.write("Logo not found.")

    if st.sidebar.button('Home'):
        st.session_state['view'] = 'home'
    # Theme Toggle Button
    st.sidebar.button('Toggle Theme', on_click=toggle_theme)

    # Button to view favorite jobs
    if st.sidebar.button('View Favorites'):
        st.session_state['view'] = 'favorites'
    
    st.sidebar.button('Logout', on_click=lambda: st.session_state.update({'authenticated': False}))

def home_frm():
    st.markdown("# PTIT Job Recommendation")

    col1, col2 = st.columns([1, 1])
    # Job Search and Filter
    title = col1.selectbox('Search Job', df['Title'].str.title().unique())
    
    # Initialize country variable
    country = None
    
    # Verify if the 'Country' column exists
    if 'Country' in df.columns:
        country = col2.selectbox('Country', df['Country'].unique())
    else:
        col2.error("'Country' column not found in the DataFrame")

    # Get recommendations
    if title and country:
        jobs = recommendation(title, country)
        if jobs:
            st.write("Recommended Jobs:")
            for idx, job in enumerate(jobs):
                with st.expander(f"{idx+1}. {job['Title'].title()}"):
                    ex_col1, ex_col2 = st.columns([1, 1])
                    with ex_col1:
                        # words = job['Description'].split()
                        # summary = ' '.join(words[:50])
                        st.markdown(f"{job['Description'][:300]}...", unsafe_allow_html=True)
                    with ex_col2:
                        st.button("Save to Favorites", on_click=save_favorite_job, args=(job,), key=f'save_{idx}')
                        st.button("Email Job Details", on_click=send_email, args=(job,), key=f'email_{idx}')
                        if st.button('View Job Details', key=f'view_{idx}'):
                            st.session_state['view'] = 'details'
                            st.session_state['job_index'] = job.name
            st.button("Export Recommendations", on_click=export_recommendations, args=(jobs,), key='export')
        else:
            st.write("No recommendations found.")

def prepare():
    # Initialize session state
    setup_session_state()
    
    # Authentication
    if not st.session_state['authenticated']:
        login_frm()
    else:
        side_bar()
        if st.session_state['view'] == 'home':
            home_frm()
        elif st.session_state['view'] == 'details':
            job_details_frm(st.session_state['job_index'])
        elif st.session_state['view'] == 'favorites':
            view_favorites_frm()

if __name__ == "__main__":
    prepare()
