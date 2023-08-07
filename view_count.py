import streamlit as st

def main():
    st.title("Streamlit View Count App")

    # Define a function to increment view count
    @st.cache(allow_output_mutation=True)
    def increment_view_count():
        return {"count": 0}

    view_count_data = increment_view_count()

    # Increment the view count when the app is accessed
    view_count_data["count"] += 1

    st.write(f"Current view count: {view_count_data['count']}")

if __name__ == "__main__":
    main()
