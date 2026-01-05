### 1. Import Libraries and connect to Snowflake
import streamlit as st
# Import the `complete` class from Cortex SDK
from snowflake.cortex import complete

import time

st.title(":material/airwave: Write Streams")

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()


### 2. Configure the User Interface
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Select a model", llm_models)

example_prompt = "What is Python?"
user_prompt = st.text_area("Enter prompt: ", example_prompt)

# Choosing the streaminf method
streaming_method = st.radio(
    "Streaming Method:",
    [
        "Direct (stream=True)",
        "Custom Generator"
    ],
    help="Choose how to stream the response"
)

### 3. Stream the LLM Response on Button Click
if st.button("Generate Response."):

    # Method 1: Direct Streaming (stream=True)
    if streaming_method == "Direct (stream=True)":
        with st.spinner(f"Generating your response with the selected model - `{model}`"):
            stream_generator = complete(
                session=session,
                model=model,
                prompt=user_prompt,
                Stream=True,
            )
            # Display the ressponse
            st.write_stream(stream_generator)

    # Method 2: Custom Stream Generator (Compatibility Mode)
    else:
        def custom_stream_generator():
            '''
            This is an alternative method for the cases where
            the generator is not compatible with 
            st.write_stream
            '''
            # output = complete(
            #     session=session,
            #     model=model,
            #     prompt=user_prompt,
            # )
            # for eachChunk in output:
            #     yield eachChunk
            #     time.sleep(0.02)  # Small delay for smooth streaming

            query = f"""
            SELECT snowflake.cortex.complete(
              '{model}',
              $$ {user_prompt} $$
            ) AS response
            """

            df = session.sql(query).collect()
            full_response = df[0]["RESPONSE"]

            for word in full_response.split(" "):
                yield word + " "
                time.sleep(0.03)           

        # Display the ressponse
        with st.spinner(f"Generating your response with the selected model - `{model}`"):
            st.write_stream(custom_stream_generator)
        st.success(f"Succesffuly recieved the response via `{streaming_method}`!!")


# Footer
st.divider()
st.caption("Day 3: Write streams | 30 Days of AI")