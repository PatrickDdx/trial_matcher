import asyncio
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool

from custom_agents.planner import search_planner
from custom_agents.ranker import ranker
from apis.clnical_trial_gov import look_for_trials
from helpers import create_paylod, format_output

from dotenv import load_dotenv

load_dotenv(override=True)

async def run_pipeline(message_desc: str, region: str = "", geo = None, distance: str = "100km"):

    if geo is not None:
        lat, lon = geo
        region = ""
    elif region is not None:
        region = region
    else:
        region = ""

    if distance == "no restriction":
        distance = "999999km"

    print("region", region)
    print("geo", geo)
    print("distance", distance)

    result = await Runner.run(search_planner, message_desc)

    facts = result.final_output

    print(facts)

    trials = look_for_trials(query_codition=facts.condition, query_intervention=facts.intervention, age=facts.age,
                             gender=facts.gender, query_location=region, geo=f"distance({lat},{lon},{distance})")

    count = trials.get("totalCount")

    print(count)

    output_text = [f"No trials found in {region or geo}. Try increasing the distance or without a Location..."]

    if count <= 10 and count > 0:
        json_trial_payload = create_paylod(trials)

        message = f"Description of the patient: {message_desc};\n\nTrials: {json_trial_payload}"

        ranks = await Runner.run(ranker, message)

        output = ranks.final_output

        output_text = []

        for t in output.ranks:
            output_text.append(f"Rank: {t.rank}\n")
            output_text.append(format_output(trials, t.nctId, json_trial_payload, (lat,lon)))
            output_text.append(f"Reason: {t.reason}\n\n")


    return output_text

#message_ = "60 year old male with nsclc and currently treated with osimertinib"
#region = "USA"
#geo = (39.7837304, -100.445882)
#distance = "200km"
#asyncio.run(run_pipeline(message_, region, geo, distance))
