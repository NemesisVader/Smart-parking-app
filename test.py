import requests

def get_mapbox_coords(address):
    access_token = "pk.eyJ1Ijoia3J5cHRvdiIsImEiOiJjbWRhOW4xdXMwZXZrMmtzYjNqcDkwZWRqIn0.y8mkMofee6LCGMvV4T_zyQ"  # Replace this
    endpoint = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"

    params = {
        'access_token': access_token,
        'limit': 1,
        'country': 'IN'
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data.get('features'):
        coords = data['features'][0]['center']  # [lon, lat]
        return coords[1], coords[0]             # (lat, lon)
    else:
        print("No results found.")
        return None, None


# 🔍 Test the function
address = "CMS, Gomti Nagar Extension, 226010"
lat, lon = get_mapbox_coords(address)
print("Final Coordinates:", lat, lon)
