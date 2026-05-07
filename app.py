# -*- coding: utf-8 -*-
"""
Created on Wed May  6 03:35:12 2026

@author: shrn1
"""

import streamlit as st

# ── Page config (must be first Streamlit command) ──────────────────────────
st.set_page_config(
    page_title="LabHelp",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar Navigation ─────────────────────────────────────────────────────
st.sidebar.title("🧪 LabHelp")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🧪 Solution Preparation",
        "🔢 Moles Calculator",
        "🔄 Unit Converter",
        "📁 Experiment Log",
        "📐 Formula Reference",
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built for lab chemists & students")

# ── Page Routing ───────────────────────────────────────────────────────────
if module == "🏠 Home":
    st.title("🧪 LabHelp")
    st.markdown("### Your all-in-one lab calculation toolkit")
    st.info("👈 Use the sidebar to navigate between modules")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🧪 Solution Preparation")
        st.caption("Molarity, dilutions, buffers, acid mixtures")
    with col2:
        st.success("🔢 Moles Calculator")
        st.caption("From mass, volume, gas, molecules")
    with col3:
        st.success("🔄 Unit Converter")
        st.caption("Concentration, mass, volume, temp, pressure")

elif module == "🧪 Solution Preparation":
    import solution_prep
    solution_prep.show()

elif module == "🔢 Moles Calculator":
    import moles
    moles.show()

elif module == "🔄 Unit Converter":
    import unit_converter
    unit_converter.show()

elif module == "📁 Experiment Log":
    import experiment_log
    experiment_log.show()

elif module == "📐 Formula Reference":
    import formula_reference
    formula_reference.show()