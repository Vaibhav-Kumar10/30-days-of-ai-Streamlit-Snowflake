import streamlit as st

st.title(":material/memory: Understanding Session State")

st.warning ("**INSTRUCTIONS:** Try clicking the + and - buttons in both columns to see the difference.")

# Create 2 columns for side-by-side comparison of both cases
column1, column2 = st.columns(2)


### --- COLUMN 1: THE WRONG WAY ---
# Using Standard Variables
with column1:
    st.header(":material/cancel: Standard Variable")
    st.write("This resets on every click.")

    # This line runs every time you click ANY button on the page.
    # It effectively erases your progress immediately.
    count_standard = 0

    # We use nested columns here to put the + and - buttons side-by-side
    sub_column_left, sub_column_right = st.columns(2)

    with sub_column_left:
        # Note: We must give every button a unique 'key'
        if st.button(":material/add:", key="standard_plus"):
            count_standard += 1

    with sub_column_right:
        if st.button(":material/remove:", key="standard_minus"):
            count_standard -= 1

    st.metric("Standard Count: ", count_standard)
    st.caption("It never gets past 1 or -1")
    st.caption("This is because `count_standard` resets to 0 before the math happens.")


### --- COLUMN 2: THE RIGHT WAY ---
# The Proper Initialization Pattern Using Session State
with column2:
    st.header(":material/check_circle: Session State")
    st.write("This memory persists.")
        
    ## 1. Initialization: Create the key only if it doesn't exist yet
    # session_state is a persistent dictionary that survives the app reruns
    if "counter_state" not in st.session_state:
        st.session_state.counter_state = 0

    # We use nested columns here as well, to put the + and - buttons side-by-side
    sub_column_left, sub_column_right = st.columns(2)

    with sub_column_left:
        ## 2. Modification: Update the dictionary value (Increment)
        # We update the value stored in the Session State dictionary
        if st.button(":material/add:", key="state_plus"):
            st.session_state.counter_state += 1

    with sub_column_right:
        ## 2. Modification: Update the dictionary value (Decrement)
        if st.button(":material/remove:", key="state_minus"):
            st.session_state.counter_state -= 1

    ## 3. Read: Display the value
    # It reads the value directly from state
    st.metric("State Count: ", st.session_state.counter_state)
    st.caption("This works because we only set the counter to 0 if it doesn't exist.")


# Footer
st.divider()
st.caption("Day 9: Understanding Session State | 30 Days of AI")
