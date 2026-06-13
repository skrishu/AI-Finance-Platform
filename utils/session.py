import streamlit as st


def login_session(user):

    st.session_state.user_id = user.id
    st.session_state.user_name = user.name
    st.session_state.logged_in = True



def logout():

    st.session_state.clear()