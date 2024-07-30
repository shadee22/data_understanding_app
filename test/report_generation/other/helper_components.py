import streamlit as st

def create_spacer(num_spacers=1):
    for _ in range(num_spacers):
        st.write("")

def create_horizontal_line():
    st.markdown("---")

def create_vertical_line():
    st.markdown("<hr>", unsafe_allow_html=True)
