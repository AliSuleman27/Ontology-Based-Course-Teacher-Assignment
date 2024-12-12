import streamlit as st
from imports import * 
from backend import execute_queries

# Loading the Ontology
ontology_file = 'Ontology.ttl'
graph = Graph()
graph.parse(ontology_file, format='ttl')

# Creating the UI
st.set_page_config(page_title="Best Teacher Finder", layout="wide")
st.markdown(
    """
    <style>
        h1 {
            text-align: center;
            color: #2B547E;
        }
        .stTextInput>div>input {
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #2B547E;
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border-radius: 12px;
        }
        .stDataFrame>div>div>div>div>table {
            font-size: 16px;
        }
        .stTabs>div>div {
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 10px;
            transition: background-color 0.3s;
        }
        .stTabs>div>div:hover {
            background-color: #e6e6e6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("\U0001F393 Ontology-Based Course Teacher Assignment")

st.markdown(
    """
    This application helps you find the **best teacher** for a particular course by analyzing skills, experience, research, domains, and degrees using semantic ontology.
    Enter the course name below to find the most relevant teacher.
    """
)

course = st.text_input("Enter the Course Name:", placeholder="e.g., NLP, IS Audit, Design Defect")
if st.button("Find Best Teacher"):
    if course:
        best_teacher, skills, relevant_experiences, research_work, depart_domain, degrees, df = execute_queries(graph,course)
        st.header(f"\U0001F4DA Best Teacher for {course}")
        st.info(f"**{best_teacher}**")
        st.subheader("\U0001F393 Degrees Matched")
        st.write(", ".join(degrees) if degrees else "No relevant degrees found.")
        st.subheader("\U0001F4E6 Domains Matched")
        st.write(", ".join(depart_domain) if depart_domain else "No relevant domains found.")
        st.subheader("\U0001F4C8 Teacher Scores")
        st.dataframe(df, use_container_width=True)
        st.subheader("\U0001F4CA Matched Skills")
        for skill in skills:
            st.write(f"- {skill}")
        st.subheader("\U0001F4BC Relevant Experience")
        experience_df = pd.DataFrame(relevant_experiences, columns=["Role", "Years", "Organization"])
        st.dataframe(experience_df, use_container_width=True)
        st.subheader("\U0001F4DA Research Work")
        st.write(", ".join(research_work) if research_work else "No relevant research found.")
    else:
        st.warning("\U000026A0 Please enter a valid course name.")

st.markdown(
    """
    <hr>
    <footer style="text-align: center; font-size: 14px;">
        \U0001F4C8 Developed by <b>Nerdy Freaks </b>. Data sourced from Ontology.
    </footer>
    """,
    unsafe_allow_html=True,
)
