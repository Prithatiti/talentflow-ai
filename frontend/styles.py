# frontend/styles.py

import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* --- GLOBAL FONTS & SETTINGS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Center all standard Streamlit headers */
        h1, h2, h3 {
            text-align: center;
            color: #0f172a;
        }

        /* --- 1. HERO SECTION STYLING --- */
        .hero-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 5rem 2rem; /* Increased vertical padding */
            border-radius: 0 0 2.5rem 2.5rem;
            margin-top: -6rem; 
            margin-left: -5rem; 
            margin-right: -5rem;
            color: white;
            text-align: center; /* Global Center alignment for Hero */
            margin-bottom: 4rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .hero-title {
            font-size: 4rem; /* Larger Title */
            font-weight: 800;
            margin-bottom: 1.5rem;
            line-height: 1.1;
            color: white !important; /* Force white over global h1 color */
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #cbd5e1; /* Lighter text for contrast */
            max-width: 800px;
            margin: 0 auto 2rem auto; /* Centered block */
            line-height: 1.6;
        }

        .highlight {
            color: #2dd4bf; /* Teal Accent */
        }

        /* --- 2. CARD STYLING (CENTERED) --- */
        .feature-card {
            background-color: white;
            padding: 2.5rem 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #f1f5f9;
            height: 100%;
            transition: all 0.3s ease;
            
            /* FLEXBOX CENTERING MAGIC */
            display: flex;
            flex-direction: column;
            align-items: center; /* Centers items horizontally */
            text-align: center;  /* Centers text inside items */
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            border-color: #2dd4bf; /* Teal border on hover */
        }

        .card-icon {
            background-color: #f0fdfa; 
            color: #0d9488; 
            width: 64px; 
            height: 64px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin-bottom: 1.5rem;
            /* No auto margin needed due to flex container */
        }

        .card-title {
            font-weight: 700;
            font-size: 1.25rem;
            color: #0f172a;
            margin-bottom: 0.75rem;
        }

        .card-text {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* --- 3. STREAMLIT WIDGET OVERRIDES --- */
        .stButton>button {
            background-color: #0d9488;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: background-color 0.2s;
            margin: 0 auto; /* Tries to center button if container allows */
            display: block;
        }
        .stButton>button:hover {
            background-color: #0f766e;
        }
        
        /* Center text inputs and areas labels if desired */
        .stTextInput label, .stTextArea label, .stNumberInput label {
            font-weight: 600;
            color: #334155;
        }
        
        </style>
    """, unsafe_allow_html=True)