### 1. Imports and Connection Setup
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_snowflake import ChatSnowflake
from pydantic import BaseModel, Field
from typing import Literal

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session

    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()


### 2. Defining the Output Schema with Pydantic
# A pydantic model to define the expected output structure
class PlantRecommendation(BaseModel):
    name: str = Field(description="Plant name")
    water: Literal["Low", "Medium", "High"] = Field(description="Water requirement")
    light: Literal["Low", "Medium", "High"] = Field(description="Light requirement")
    difficulty: Literal["Beginner", "Intermediate", "Expert"] = Field(
        description="Care difficulty level"
    )
    care_tips: str = Field(description="Brief care instructions")


### 3. Creating the Parser
output_parser = PydanticOutputParser(pydantic_object=PlantRecommendation)


### 4. Creating the Prompt Template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a plant expert. {format_instructions}"),
        (
            "human",
            "Recommend a plant for: {location}, {experience} experience, {space} space",
        ),
    ]
)

### 5. Building the Chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
chain = prompt_template | llm | output_parser
# The | operator connects the prompt output to the LLM.

### 6. Building the Streamlit UI
st.title(":material_potted_plant: Plant Recommender")
location = st.text_input("Location:", "Apartment in Seattle")
experience = st.selectbox("Experience:", ["Beginner", "Intermediate", "Expert"])
space = st.text_input("Space:", "Small desk")


### 7. Invoking the Chain and Displaying Results
if st.button("Get Recommendation"):
    result = chain.invoke(
        {
            "location": location,
            "experience": experience,
            "space": space,
            "format_instructions": output_parser.get_format_instructions(),
            # it generates a JSON schema instructions that tell the LLM exactly how to format its response.
        }
    )

    st.subheader(f":material/eco: {result.name}")
    column1, column2, column3 = st.columns(3)
    column1.metric("Water", result.water)
    column2.metric("Light", result.light)
    column3.metric("Difficulty", result.difficulty)
    st.info(f"**Care:** {result.care_tips}")

    with st.expander(":material/description: See raw JSON response"):
        st.json(result.model_dump())
        # Converts the Pydantic object back to a dictionary for JSON display.


st.divider()
st.caption("Day 30: Structured Output with Pydantic | 30 Days of AI with Streamlit")
