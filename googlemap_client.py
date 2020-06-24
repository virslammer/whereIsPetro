
'''
------------------
GOOGLE MAP CLIENT CLASS 
-----------------
'''
from urllib.parse import urlencode
import requests 
class GoogleMapClient(object):

    lat = None 
    lng = None 
    place_id = None
    data_type = 'json'
    location_query = None
    api_key = None
    def __init__(self, location_query=None, api_key=None,  lat=None,lng=None,*args, **kwargs):

        if api_key==None:
            raise Exception('API key is required')
        self.api_key = api_key
        self.location_query = location_query
        self.lat = lat 
        self.lng = lng
        if self.location_query != None:
            self.extract_lat_lng(location_query)
            self.extract_place_id(location_query)
    
    def __str__(self):
        return f'{self.lat,self.lng}'

    def extract_lat_lng(self, location=None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f'https://maps.googleapis.com/maps/api/geocode/{self.data_type}'
        params = {
            'address':f"{loc_query}",
            'key':self.api_key
        }
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        data = r.json()
        try:
            self.lat = data['results'][0]['geometry']['location']["lat"]
            self.lng = data['results'][0]['geometry']['location']["lng"]
        except:
            pass

        return self.lat,self.lng
    
    def extract_place_id(self, location=None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f'https://maps.googleapis.com/maps/api/geocode/{self.data_type}'
        params = {
            'address':f"{loc_query}",
            'key':self.api_key
        }
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        data = r.json()
        try:
            self.place_id = data['results'][0]['place_id']

        except:
            pass
        return self.place_id
    def extract_place_id_by_latlng(self,lat=None,lng=None):
        latlng = f'{self.lat},{self.lng}'
        endpoint = f'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'latlng':latlng,
            'key':self.api_key
        }
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        data = r.json()
        try:
            self.place_id = data['results'][0]['place_id']

        except:
            pass
        return self.place_id 
    def get_detail(self, location=None,place_id=None):
        place_id = self.extract_place_id()
        if location != None:
            place_id = self.extract_place_id(location)
        endpoint = f'https://maps.googleapis.com/maps/api/place/details/{self.data_type}'
        params = {
            'key':self.api_key,
            'place_id':place_id,
        }
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def get_detail_by_latlng(self, lat=None,lng=None,place_id=None):
        place_id = self.extract_place_id_by_latlng()
        if lat != None and lng != None:
            place_id = self.extract_place_by_latlng(lat,lng)
        endpoint = f'https://maps.googleapis.com/maps/api/place/details/{self.data_type}'
        params = {
            'key':self.api_key,
            'place_id':place_id,
        }
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def search_place(self,input='Cay xang',use_locationbias=False,use_circular=False, radius=1000, location=None):
        lat,lng = self.lat,self.lng
        if location != None :
            lat,lng = extract_lat_lng(location)
        endpoint = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/{self.data_type}'
        
        params = {
            'key':self.api_key,
            'input':f'{input}',
            'inputtype':'textquery',
            'fields':'formatted_address,geometry,name,place_id'
        }
        if use_locationbias:
            locationbias = f"point:{lat},{lng}"

            if use_circular: 
                locationbias= f"circle:{radius}@{lat},{lng}"
            params['locationbias'] = locationbias
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def search_nearby(self,keyword, type=None,radius=1000):

        endpoint = f'https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}'
        params = {
            'key':self.api_key,
            'location':f"{self.lat},{self.lng}",
            'radius':radius,
            'keyword':f'{keyword}',
            'inputtype':'textquery',
            
        }
        if type != None:
            params['type'] = type
        url = f'{endpoint}?{urlencode(params)}'
        r = requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()



