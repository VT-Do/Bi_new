import streamlit as st

# Initialize view count
view_count = 0

# Check if 'view_count' exists in Streamlit's session state
if 'view_count' not in st.session_state:
    st.session_state.view_count = view_count

# Increment view count when the app is accessed
st.session_state.view_count += 1

# Streamlit app layout
def main():
    st.title("Streamlit View Count App")
    
    st.write("This app keeps track of the number of views.")
    
    st.write(f"Current view count: {st.session_state.view_count}")

if __name__ == "__main__":
    main()
