import streamlit as st
import pandas as pd

# Load data
df = pd.read_pickle('df.pkl')
similarity = pd.read_pickle('similarity.pkl')

def recommendation(title, num_recommendations=20):
    try:
        idx = df[df['Title'] == title].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:num_recommendations]
        
        recommended_jobs = [df.iloc[i[0]] for i in distances]
        return recommended_jobs
    except IndexError:
        return []

def job_details(index):
    job = df.iloc[index]
    st.write(f"## {job['Title']}")
    # st.write(f"**Description:** {job['Description']}")
    # st.write(f"**Requirements:** {job['Requirements']}")

    st.markdown(f"**Description:** {job['Description']}", unsafe_allow_html=True)
    st.markdown(f"**Requirements:** {job['Requirements']}", unsafe_allow_html=True)

    st.write(f"**Location:** {job['City']}, {job['State']}, {job['Country']}")
    st.markdown("[Back to recommendations](http://localhost:8501/#g%E1%BB%A3i-%C3%BD-vi%E1%BB%87c-l%C3%A0m-ptit)")

# Streamlit app
# st.image('logo.jpg', width=50)  # Adjust the path and width as needed
st.markdown("# [Gợi ý việc làm PTIT](#gợi-ý-việc-làm-ptit)")

# Check for job_id in query parameters
query_params = st.query_params
if 'job_id' in query_params:
    job_index = int(query_params['job_id'][0])
    job_details(job_index)
else:
    # st.title('Gợi ý việc làm PTIT')

    # Selectbox for job titles
    title = st.selectbox('Search Job', df['Title'])

    # Get recommendations
    if title:
        jobs = recommendation(title)
        if jobs:
            st.write("Recommended Jobs:")
            for job in jobs:
                job_url = f"/?job_id={job['index']}"
                st.markdown(f"- [{job['Title']}]({job_url})")
        else:
            st.write("No recommendations found.")
