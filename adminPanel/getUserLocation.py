import requests


def get_location(ip_adrs):
    response = requests.get(f'https://ipapi.co/{ip_adrs}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data