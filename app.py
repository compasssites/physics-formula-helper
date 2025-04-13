import streamlit as st
import pandas as pd
import re
import requests
from io import BytesIO

# Initialize session state for page and search terms
if 'page' not in st.session_state:
    st.session_state.page = "Formulas"
if 'search_term_formulas' not in st.session_state:
    st.session_state.search_term_formulas = ""
if 'search_term_constants' not in st.session_state:
    st.session_state.search_term_constants = ""
if 'search_term_scientists' not in st.session_state:
    st.session_state.search_term_scientists = ""
if 'search_term_dimensions' not in st.session_state:
    st.session_state.search_term_dimensions = ""
if 'clear_counter_formulas' not in st.session_state:
    st.session_state.clear_counter_formulas = 0
if 'clear_counter_constants' not in st.session_state:
    st.session_state.clear_counter_constants = 0
if 'clear_counter_scientists' not in st.session_state:
    st.session_state.clear_counter_scientists = 0
if 'clear_counter_dimensions' not in st.session_state:
    st.session_state.clear_counter_dimensions = 0

# Sidebar navigation with clickable text links
st.sidebar.title("Navigation")

# Custom CSS for navigation links and other styles
st.markdown(
    """
    <style>
    .nav-link {
        display: block;
        padding: 8px 0;
        font-size: 18px;
        color: #1E90FF;
        text-decoration: none;
        cursor: pointer;
    }
    .nav-link:hover {
        text-decoration: underline;
        color: #FF4500;
    }
    /* Uniform LaTeX size for all pages */
    .katex-html {
        font-size: 24px !important;
        vertical-align: middle;
    }
    /* Style for labels to match LaTeX */
    .label {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader-with-symbol {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .stButton>button {
        background: none;
        border: none;
        padding: 8px 0;
        font-size: 18px;
        color: #1E90FF;
        text-decoration: none;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    .stButton>button:hover {
        text-decoration: underline;
        color: #FF4500;
    }
    /* Style the clear button */
    .stButton.clear-button>button {
        height: 38px;
        padding: 0 16px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f0f0f0;
        color: #888;
        cursor: pointer;
    }
    @media (max-width: 600px) {
        .stButton.clear-button>button {
            height: 36px;
            padding: 0 12px;
            font-size: 14px;
        }
    }
    /* Ensure sidebar is visible on mobile */
    @media (max-width: 600px) {
        .stSidebar {
            display: block !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Helper function to extract and render LaTeX parts
def render_latex_field(text):
    # Find all LaTeX expressions (e.g., $[M L^2 T^{-2}]$)
    latex_parts = re.findall(r'\$[^\$]+\$', text)
    if not latex_parts:
        # No LaTeX, render as plain text
        st.write(text)
        return

    # Split the text into parts around LaTeX expressions
    parts = re.split(r'(\$[^\$]+\$)', text)
    for part in parts:
        if part in latex_parts:
            # Render LaTeX in display mode (remove the $ signs and use $$...$$)
            latex_content = part.strip('$')
            st.markdown(f"$${latex_content}$$", unsafe_allow_html=True)
        else:
            # Render plain text
            if part.strip():
                st.write(part)

# Helper function to fetch and display images (bypass CORS)
def display_image(url, width=200):
    try:
        # Fetch the image using requests
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad status codes
        image_data = BytesIO(response.content)
        st.image(image_data, width=width)
    except Exception as e:
        st.warning(f"Failed to load image: {e}")
        # Fallback to placeholder image
        st.image("https://via.placeholder.com/200x200.png?text=Image+Not+Found", width=width)

# Navigation links styled as clickable text
if st.sidebar.button("Formulas", key="nav_formulas", help="Go to Formulas page"):
    st.session_state.page = "Formulas"
    st.session_state.search_term_formulas = ""
    st.session_state.clear_counter_formulas += 1
    st.rerun()
if st.sidebar.button("Constants", key="nav_constants", help="Go to Constants page"):
    st.session_state.page = "Constants"
    st.session_state.search_term_constants = ""
    st.session_state.clear_counter_constants += 1
    st.rerun()
if st.sidebar.button("Scientists", key="nav_scientists", help="Go to Scientists page"):
    st.session_state.page = "Scientists"
    st.session_state.search_term_scientists = ""
    st.session_state.clear_counter_scientists += 1
    st.rerun()
if st.sidebar.button("Dimensions", key="nav_dimensions", help="Go to Dimensions page"):
    st.session_state.page = "Dimensions"
    st.session_state.search_term_dimensions = ""
    st.session_state.clear_counter_dimensions += 1
    st.rerun()

# Page 1: Formulas
if st.session_state.page == "Formulas":
    try:
        formulas = pd.read_csv('formulas.csv').to_dict('records')
        st.write(f"Loaded {len(formulas)} formulas from CSV.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        formulas = []

    st.title("Physics Formula Helper")
    st.write("Search and explore Class 11 & 12 NCERT Physics formulas for NEET prep!")

    col1, col2 = st.columns([8, 2], vertical_alignment="center")
    with col1:
        search_input = st.text_input(
            "Search by name, chapter, or concept (e.g., 'Newton', 'Laws of Motion', 'Force')",
            value=st.session_state.search_term_formulas,
            key=f"search_input_formulas_{st.session_state.clear_counter_formulas}",
            label_visibility="visible"
        )
        st.session_state.search_term_formulas = search_input
    with col2:
        if st.button("Clear", key="clear_button_formulas", help="Clear search term", type="secondary"):
            st.session_state.search_term_formulas = ""
            st.session_state.clear_counter_formulas += 1
            st.rerun()

    search_term = st.session_state.search_term_formulas.strip().lower()
    st.write(f"Current search term: '{search_term}'")

    matching_formulas = 0
    for formula in formulas:
        formula_name = str(formula['Formula Name']).lower()
        chapter_name = str(formula['Chapter Name']).lower()
        key_concepts = str(formula['Key Concepts']).lower()

        if (not search_term or
            search_term in formula_name or
            search_term in chapter_name or
            search_term in key_concepts):
            matching_formulas += 1
            st.subheader(formula['Formula Name'])
            st.markdown("<div class='label'>Definition:</div>", unsafe_allow_html=True)
            st.write(formula['Definition'])
            if formula['Formula'] != "-":
                st.markdown("<div class='label'>Formula:</div>", unsafe_allow_html=True)
                st.markdown(f"$${formula['Formula']}$$", unsafe_allow_html=True)
            
            if 'Variables' in formula and formula['Variables'] != "-":
                st.markdown("<div class='label'>Variables:</div>", unsafe_allow_html=True)
                st.markdown(formula['Variables'], unsafe_allow_html=True)

            with st.expander("More Details"):
                st.markdown("<div class='label'>Chapter:</div>", unsafe_allow_html=True)
                st.write(formula['Chapter Name'])
                st.markdown("<div class='label'>Unit:</div>", unsafe_allow_html=True)
                st.write(formula['Unit'])
                st.markdown("<div class='label'>Example:</div>", unsafe_allow_html=True)
                st.markdown(formula['Brief Example'], unsafe_allow_html=True)
                st.markdown("<div class='label'>Tip:</div>", unsafe_allow_html=True)
                st.markdown(formula['Remarks/Tips'], unsafe_allow_html=True)
                st.markdown("<div class='label'>Concepts:</div>", unsafe_allow_html=True)
                st.write(formula['Key Concepts'])

    st.write(f"Found {matching_formulas} matching formulas.")
    if not search_term:
        st.write("Enter a search term to filter, or browse all formulas above!")

# Page 2: Constants
elif st.session_state.page == "Constants":
    try:
        constants = pd.read_csv('constants.csv').to_dict('records')
        st.write(f"Loaded {len(constants)} constants from CSV.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        constants = []

    st.title("Physical Constants")
    st.write("A quick reference for important physical constants used in Class 11 & 12 NCERT Physics.")

    col1, col2 = st.columns([8, 2], vertical_alignment="center")
    with col1:
        search_input = st.text_input(
            "Search by name, symbol, or usage (e.g., 'Planck', 'h', 'quantum')",
            value=st.session_state.search_term_constants,
            key=f"search_input_constants_{st.session_state.clear_counter_constants}",
            label_visibility="visible"
        )
        st.session_state.search_term_constants = search_input
    with col2:
        if st.button("Clear", key="clear_button_constants", help="Clear search term", type="secondary"):
            st.session_state.search_term_constants = ""
            st.session_state.clear_counter_constants += 1
            st.rerun()

    search_term = st.session_state.search_term_constants.strip().lower()
    st.write(f"Current search term: '{search_term}'")

    matching_constants = 0
    for constant in constants:
        constant_name = str(constant['Constant Name']).lower()
        symbol = str(constant['Symbol']).lower()
        definition = str(constant['Definition']).lower()
        usage = str(constant['Usage']).lower()

        if (not search_term or
            search_term in constant_name or
            search_term in symbol or
            search_term in definition or
            search_term in usage):
            matching_constants += 1
            # Split Constant Name into name and symbol
            name_parts = constant['Constant Name'].split(',')
            if len(name_parts) == 2:
                name_text = name_parts[0].strip()
                symbol_text = name_parts[1].strip()  # e.g., $c$
            else:
                name_text = constant['Constant Name']
                symbol_text = constant['Symbol']  # Fallback to Symbol column

            # Render name and symbol in display mode
            st.markdown(
                f"<div class='subheader-with-symbol'>{name_text}<br>",
                unsafe_allow_html=True
            )
            st.markdown(f"$${symbol_text}$$", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='label'>Value:</div>", unsafe_allow_html=True)
            st.markdown(f"$${constant['Value']}$$", unsafe_allow_html=True)
            st.markdown("<div class='label'>Unit:</div>", unsafe_allow_html=True)
            st.write(constant['Unit'])  # Unit might not always be LaTeX, so render as text
            st.markdown("<div class='label'>Definition:</div>", unsafe_allow_html=True)
            st.write(constant['Definition'])
            st.markdown("<div class='label'>Usage:</div>", unsafe_allow_html=True)
            st.write(constant['Usage'])
            st.markdown("<div class='label'>Likely MCQ:</div>", unsafe_allow_html=True)
            render_latex_field(constant['Likely MCQ'])

    st.write(f"Found {matching_constants} matching constants.")
    if not search_term:
        st.write("Enter a search term to filter, or browse all constants above!")

# Page 3: Scientists
elif st.session_state.page == "Scientists":
    try:
        scientists = pd.read_csv('scientists.csv').to_dict('records')
        st.write(f"Loaded {len(scientists)} scientists from CSV.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        scientists = []

    st.title("Famous Scientists in Physics")
    st.write("Key scientists from Class 11 & 12 NCERT Physics, useful for NEET MCQs.")

    col1, col2 = st.columns([8, 2], vertical_alignment="center")
    with col1:
        search_input = st.text_input(
            "Search by name, year, or contribution (e.g., 'Einstein', '1905', 'relativity')",
            value=st.session_state.search_term_scientists,
            key=f"search_input_scientists_{st.session_state.clear_counter_scientists}",
            label_visibility="visible"
        )
        st.session_state.search_term_scientists = search_input
    with col2:
        if st.button("Clear", key="clear_button_scientists", help="Clear search term", type="secondary"):
            st.session_state.search_term_scientists = ""
            st.session_state.clear_counter_scientists += 1
            st.rerun()

    search_term = st.session_state.search_term_scientists.strip().lower()
    st.write(f"Current search term: '{search_term}'")

    matching_scientists = 0
    for scientist in scientists:
        name = str(scientist['Name']).lower()
        year = str(scientist['Year']).lower()
        contribution = str(scientist['Contribution']).lower()
        mcq = str(scientist['Likely MCQ']).lower()
        tip = str(scientist['Tip/Suggestion']).lower()

        if (not search_term or
            search_term in name or
            search_term in year or
            search_term in contribution or
            search_term in mcq or
            search_term in tip):
            matching_scientists += 1
            st.subheader(scientist['Name'])
            # Use the display_image function to fetch and display the image
            display_image(scientist['Image URL'], width=200)
            st.markdown("<div class='label'>Year:</div>", unsafe_allow_html=True)
            st.write(scientist['Year'])
            st.markdown("<div class='label'>Contribution:</div>", unsafe_allow_html=True)
            render_latex_field(scientist['Contribution'])
            st.markdown("<div class='label'>Likely MCQ:</div>", unsafe_allow_html=True)
            render_latex_field(scientist['Likely MCQ'])
            st.markdown("<div class='label'>Memory Tip:</div>", unsafe_allow_html=True)
            st.write(scientist['Tip/Suggestion'])

    st.write(f"Found {matching_scientists} matching scientists.")
    if not search_term:
        st.write("Enter a search term to filter, or browse all scientists above!")

# Page 4: Dimensions
elif st.session_state.page == "Dimensions":
    try:
        dimensions = pd.read_csv('dimensions.csv').to_dict('records')
        st.write(f"Loaded {len(dimensions)} dimensions from CSV.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        dimensions = []

    st.title("Dimensions of Physical Quantities")
    st.write("A quick reference for dimensions of common physical quantities and constants in Class 11 & 12 NCERT Physics.")

    col1, col2 = st.columns([8, 2], vertical_alignment="center")
    with col1:
        search_input = st.text_input(
            "Search by entity or formula (e.g., 'Force', 'Velocity', 'Planck')",
            value=st.session_state.search_term_dimensions,
            key=f"search_input_dimensions_{st.session_state.clear_counter_dimensions}",
            label_visibility="visible"
        )
        st.session_state.search_term_dimensions = search_input
    with col2:
        if st.button("Clear", key="clear_button_dimensions", help="Clear search term", type="secondary"):
            st.session_state.search_term_dimensions = ""
            st.session_state.clear_counter_dimensions += 1
            st.rerun()

    search_term = st.session_state.search_term_dimensions.strip().lower()
    st.write(f"Current search term: '{search_term}'")

    matching_dimensions = 0
    for dimension in dimensions:
        entity = str(dimension['Entity']).lower()
        formula = str(dimension['Formula']).lower()
        dimensions_str = str(dimension['Dimensions']).lower()
        tip = str(dimension['Tip/Hack']).lower()
        mcq = str(dimension['Likely MCQ']).lower()

        if (not search_term or
            search_term in entity or
            search_term in formula or
            search_term in dimensions_str or
            search_term in tip or
            search_term in mcq):
            matching_dimensions += 1
            st.subheader(dimension['Entity'])
            if dimension['Formula'] != "-":
                st.markdown("<div class='label'>Formula:</div>", unsafe_allow_html=True)
                # Check if Formula needs LaTeX rendering
                if '$' in dimension['Formula']:
                    latex_content = dimension['Formula'].strip('$')
                    st.markdown(f"$${latex_content}$$", unsafe_allow_html=True)
                else:
                    st.write(dimension['Formula'])
            st.markdown("<div class='label'>Dimensions:</div>", unsafe_allow_html=True)
            st.markdown(f"$${dimension['Dimensions']}$$", unsafe_allow_html=True)
            st.markdown("<div class='label'>Memory Tip/Hack:</div>", unsafe_allow_html=True)
            st.write(dimension['Tip/Hack'])
            st.markdown("<div class='label'>Likely MCQ:</div>", unsafe_allow_html=True)
            render_latex_field(dimension['Likely MCQ'])

    st.write(f"Found {matching_dimensions} matching dimensions.")
    if not search_term:
        st.write("Enter a search term to filter, or browse all dimensions above!")