from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(override=True)

class Trial_Format(BaseModel):
    rank: int = Field(description="The rank of the trial.")
    nctId: str = Field(description="The nctId of the trial")
    reason: str = Field("The reason for the decision")

class Rank_Format(BaseModel):
    ranks: list[Trial_Format] = Field(description="Ranked list of the trials")


INSTRUCTIONS = """You are a medical assistant. Given a free text description of a patient and a list of clinical trials, evaluate if the patient is an appropriate fit for the trials.
Go through the trials one by one and give a short reason why the patient might be a fit or why not. Then rank the trials in order, starting with the one that best fits the patient.
Return only the rank, the nctId and the reason for each trial:
1. nctId, reason
2. nctId, reason
..."""

ranker = Agent(
    name="Trial ranker",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Rank_Format
)