def create_paylod(trials):
    lean_trials_data = []
    for trial in trials.get("studies", []):
        ps = trial.get("protocolSection", {})
        idm = ps.get("identificationModule", {})
        stm = ps.get("statusModule", {})
        dsm = ps.get("descriptionModule", {})
        elm = ps.get("eligibilityModule", {})

        record = {
            "nctId": idm.get("nctId"),
            "briefTitle": idm.get("briefTitle"),
            "officialTitle": idm.get("officialTitle"),

            "status": stm.get("overallStatus"),

            "summary": dsm.get("briefSummary"),

            "eligibilityCriteria": elm.get("eligibilityCriteria"),
            "age": {"min": elm.get("minimumAge", "None"), "max": elm.get("maximumAge", "None")},
            "sex": elm.get("sex")

        }

        lean_trials_data.append(record)

    return lean_trials_data


from geopy.distance import geodesic

def calculate_distance_to_point(point_a, point_constant):
    """the ouput of the 2 print statements looks like this:
        {'lat': 33.70918, 'lon': -117.95367}
        (33.70918, -117.95367)
        {'lat': 33.80307, 'lon': -118.07256}
        (33.80307, -118.07256)
        {'lat': 34.05223, 'lon': -118.24368}
        (34.05223, -118.24368)
    """
    # print(point_a)
    try:
        point_coords = (point_a["lat"], point_a["lon"])
        # print(point_coords)

        distance_km = geodesic(point_coords, point_constant).km
    except Exception as e:
        # print(f"Error when trying to cal the distance or extracting the point: {e}")
        distance_km = 999_999

    return distance_km

def find_trial(trials: dict, id: str) -> dict | None:
    target = id.strip().upper()
    for trial in trials.get("studies", []):
        ps = trial.get("protocolSection", {})
        idm = ps.get("identificationModule", {})

        nctId = idm.get("nctId").strip().upper()

        if nctId == target:
            return trial
    return None


def find_locations(trials: dict, id: str, point=None):
    trial_by_id = find_trial(trials, id)

    ps = trial_by_id.get("protocolSection", {})
    clm = ps.get("contactsLocationsModule")
    loc = clm.get("locations")

    locations = []

    for i in loc:
        location_dict = {}
        location_dict["facility"] = i.get("facility")
        location_dict["geoPoint"] = i.get("geoPoint")

        locations.append(location_dict)

    #print(locations)
    try:
        #point = (51.4641, 6.8771)
        sorted_locations = sorted(locations, key=lambda loc: calculate_distance_to_point(loc["geoPoint"], point))
    except Exception as e:
        #print(f"Error when calculatin distance: {e}")
        sorted_locations = locations

    return sorted_locations

def get_clean_trial(target_id: str, json_trial_payload):
    for trial in json_trial_payload:
        id = trial.get("nctId").strip().upper()
        if id == target_id.strip().upper():
            return trial
    return None


def format_output(trials: dict, target_id: str, clean_trials_payload: dict, point=None):
    trial = get_clean_trial(target_id, clean_trials_payload)

    trial_info = ""

    trial_info += f"nctId: {trial.get("nctId")}\n"
    trial_info += f"Title: {trial.get("briefTitle")}\n"
    trial_info += f"Status: {trial.get("status")}\n"

    locations = find_locations(trials, target_id, point)

    trial_info += f"Locations: "
    for l in locations[:5]:
        facility = l.get("facility")
        trial_info += f"{facility}, "

    return trial_info