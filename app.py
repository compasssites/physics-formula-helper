import streamlit as st
import pandas as pd

# Initialize session state for the search term
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

# Load the CSV data
try:
    formulas = pd.read_csv('formulas.csv').to_dict('records')
    # st.write(f"Loaded {len(formulas)} formulas from CSV.")  # Confirm data is loaded
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    formulas = []

# App title and description
st.title("Physics Formula Helper")
st.write("Search and explore Class 11 & 12 NCERT Physics formulas for NEET prep!")

# Search bar with clear button
col1, col2 = st.columns([10, 1])  # Allocate space: 10 parts for input, 1 for button
with col1:
    search_input = st.text_input(
        "Search by name, chapter, or concept (e.g., 'Newton', 'Laws of Motion', 'Force')",
        value=st.session_state.search_term,
        key="search_input"
    )
with col2:
    if st.button("✕", key="clear_button"):  # Clear button with '✕' symbol
        st.session_state.search_term = ""
        st.rerun()  # Rerun the app to refresh with an empty search term

# Update session state with the new search input
if search_input != st.session_state.search_term:
    st.session_state.search_term = search_input

# Process the search term
search_term = st.session_state.search_term.strip().lower()

# Debug: Show the current search term
st.write(f"Current search term: '{search_term}'")

# Filter and display matching formulas
matching_formulas = 0
for formula in formulas:
    formula_name = str(formula['Formula Name']).lower()
    chapter_name = str(formula['Chapter Name']).lower()
    key_concepts = str(formula['Key Concepts']).lower()

    # Check if the search term matches any field (or show all if search is empty)
    if (not search_term or
        search_term in formula_name or
        search_term in chapter_name or
        search_term in key_concepts):
        matching_formulas += 1
        st.subheader(formula['Formula Name'])
        st.write(f"**Definition**: {formula['Definition']}")
        if formula['Formula'] != "-":
            st.markdown(formula['Formula'], unsafe_allow_html=True)
        
        with st.expander("More Details"):
            st.write(f"**Chapter**: {formula['Chapter Name']}")
            st.write(f"**Unit**: {formula['Unit']}")
            st.write("**Example**:")
            st.markdown(formula['Brief Example'], unsafe_allow_html=True)
            st.write("**Tip**:")
            st.markdown(formula['Remarks/Tips'], unsafe_allow_html=True)
            st.write(f"**Concepts**: {formula['Key Concepts']}")

# Debug: Show the number of matches
st.write(f"Found {matching_formulas} matching formulas.")

# Prompt if no search term is entered
if not search_term:
    st.write("Enter a search term to filter, or browse all formulas above!")