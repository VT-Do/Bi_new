import streamlit as st
from streamlit import SessionState

def main():
    st.title("Streamlit View Count App")

    # Initialize the SessionState class with a default value for view_count
    session_state = SessionState.get(view_count=0)

    # Increment the view count when the app is accessed
    session_state.view_count += 1

    st.write(f"Current view count: {session_state.view_count}")

if __name__ == "__main__":
    main()
