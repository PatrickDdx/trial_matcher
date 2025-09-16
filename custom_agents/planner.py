from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True) #replace with st.secrets

class KeyFacts(BaseModel):
    condition: str = Field(description="Conditions or disease the person has (for example, breast cancer or high blood pressure).")
    intervention: str = Field(description="Intervention / Treatment (for example, radiation therapy or low fat diet).")
    age: int = Field(description="Age of the person in years.")
    gender: str = Field(description="Gender of the person (MALE or FEMALE).")
    location: str = Field(description="The location where the trial should be (search by address, city, state, or country).")


INSTRUCTIONS = """You are a medical assistant. Given a free text, you extract the key facts and fill them into the schema.
Return a json only - no explanations, no comments. The schema: condition, intervention, age, gender, location.
The output will be used to search clinicaltrials.gov via their API. 
Use Boolean operators (AND / OR / NOT) and Grouping operators ( () ) if necessary.
The location must be an address, city, state, or country.
The output must be in English, regardless of the input language."""

search_planner = Agent(
    name="Query builder helper",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=KeyFacts
)

async def main():
    #message = "55 year old man with nsclc and currently treated with Osimertinib" # -> condition='non-small cell lung cancer (NSCLC)' intervention='Osimertinib' age=55 gender='MALE'
    message = "I have a 55-year-old female with metastatic triple-negative breast cancer. She has progressed after first-line carboplatin/paclitaxel and immunotherapy with pembrolizumab. Looking for trials with novel antibody-drug conjugates or PARP inhibitors, preferably in the Northeast US."

    result = await Runner.run(search_planner, message)

    print(result.final_output)

#asyncio.run(main())