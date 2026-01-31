### 1. Snowflake Connection Setup
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_snowflake import ChatSnowflake

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session

    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()


### 2. Creating a PromptTemplate
prompt_template = PromptTemplate.from_template(
    """
    You are an expert social media manager. Generate a LinkedIn post based on the following:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points.
    """
)

### 3. Creating the LLM and Chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
# Using LCEL (LangChain Expression Language), chain can be created as:
chain = prompt_template | llm
# The | operator connects the prompt output to the LLM.


### 4. Building the Streamlit UI
st.title(":material/post: LinkedIn Post Generator")
content = st.text_input(
    "Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview"
)
tone = st.selectbox("TONE: ", ["Professional", "Natural", "Casual", "Funny", "Simple"])
word_count = st.slider("Approximate WORD COUNT: ", 50, 300, 100)


### 5. Invoking the Chain
if st.button("Generate Post"):
    result = chain.invoke({"content": content, "tone": tone, "word_count": word_count})
    st.subheader("Generated Post:")
    st.markdown(result.content)


st.divider()
st.caption("Day 29: LangChain Basics | 30 Days of AI with Streamlit")
