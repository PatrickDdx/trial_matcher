import requests


def build_advanced_filters(age=None, sex=None):
    # Build the advanced filter string
    advanced_filters = []

    if age is not None:
        advanced_filters.append(
            f"(AREA[MinimumAge]RANGE[MIN, {age} years] AND AREA[MaximumAge]RANGE[{age} years, MAX]) OR AREA[MinimumAge]RANGE[MIN, {age} years]")

    if sex and sex.upper() in ["MALE", "FEMALE"]:
        advanced_filters.append(f"AREA[Sex]({sex.upper()} OR ALL)")

    return advanced_filters

def look_for_trials(
    query_codition: str = "",
    query_intervention: str = "",
    age = None,
    gender: str = "ALL",
    query_location: str = "",
    overall_status: str = "RECRUITING",
    geo: str = None,
):
    """
    query clinicaltrials.gov API to get a json af available trials
    query_condition: "Conditions or disease" query
    query_intervention: "Intervention / treatment" query
    overall_status:  ACTIVE_NOT_RECRUITING ┃ COMPLETED ┃ ENROLLING_BY_INVITATION ┃ NOT_YET_RECRUITING ┃ RECRUITING ┃ SUSPENDED ┃ TERMINATED ┃ WITHDRAWN ┃ AVAILABLE ┃ NO_LONGER_AVAILABLE ┃ TEMPORARILY_NOT_AVAILABLE ┃ APPROVED_FOR_MARKETING ┃ WITHHELD ┃ UNKNOWN
    query_location: "Location terms" query

    """
    # The search query
    query_params = {
        "query.titles": "",
        "query.term": "",
        "query.cond": query_codition,
        "query.intr": query_intervention,
        "query.locn": query_location,
        "filter.overallStatus": overall_status,
        "filter.geo": geo, #Examples: distance(39.0035707,-77.1013313,50mi)
        "pageSize": 10,
        "fields": "NCTId,BriefTitle,OfficialTitle,OverallStatus,BriefSummary,EligibilityModule,ContactsLocationsModule", #Phases?
        #"format": "csv",
        "sort": "@relevance",
        "countTotal": "true",
    }

    # Build the advanced filter string
    advanced_filters = build_advanced_filters(age, gender)#, gender)

    if advanced_filters:
        query_params["filter.advanced"] = " AND ".join(advanced_filters)
        #print(query_params["filter.advanced"])

    # The API endpoint
    url = "https://clinicaltrials.gov/api/v2/studies"

    print(url, query_params)

    data = {}

    try:
        # Send the GET request
        response = requests.get(url, params=query_params)
        response.raise_for_status()

        data = response.json()

    except Exception as e:
        print(f"An error occurred: {e}")

    return data if data else {}