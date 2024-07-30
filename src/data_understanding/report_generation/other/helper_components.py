import streamlit as st

def spacer(num_spacers=1):
    for _ in range(num_spacers):
        st.write("#")
        st.write("#")


def create_horizontal_line():
    st.markdown("---")

def create_vertical_line():
    st.markdown("<hr>", unsafe_allow_html=True)
