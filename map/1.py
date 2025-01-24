from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_province_from_coords(latitude, longitude):
    geolocator = Nominatim(user_agent="YourAppName/1.0 (contact@yourdomain.com)")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            
            address = location.raw.get('address', {})
            province = address.get('state', address.get('city', None))  
            return province
    except GeocoderTimedOut:
        
        return get_province_from_coords(latitude, longitude)  
    
    return None

latitude = 38.10667944528146  
longitude = 48  

province = get_province_from_coords(latitude, longitude)
print(province)
