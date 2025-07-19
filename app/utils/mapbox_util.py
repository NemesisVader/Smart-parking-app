import requests

def get_mapbox_coords(address):
    """
    Get (lat, lon) for a given address using Mapbox Geocoding API.
    """
    token = "pk.eyJ1Ijoia3J5cHRvdiIsImEiOiJjbWRhOW4xdXMwZXZrMmtzYjNqcDkwZWRqIn0.y8mkMofee6LCGMvV4T_zyQ"
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {
        'access_token': token,
        'limit': 1,
    }

    try:
        res = requests.get(url, params=params, timeout=4)
        data = res.json()
        if 'features' in data and len(data['features']) > 0:
            lon, lat = data['features'][0]['center']
            return lat, lon
    except Exception as e:
        print(f"[Mapbox Error] {e}")

    return None, None
