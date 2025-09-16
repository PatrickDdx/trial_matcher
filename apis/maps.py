from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-geocoder")

def place_to_coordinates(place):
    location = geolocator.geocode(place)
    print(f"returned location: {location}")
    return location.address, location.latitude, location.longitude


#print(place_to_coordinates("Germany"))
