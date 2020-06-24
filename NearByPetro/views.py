from django.shortcuts import render
from django.http import JsonResponse
from googlemap_client import GoogleMapClient

import json

# Create your views here.
def Index(request):

    context = {}
    return render(request,'index.html',context)

def ShowNearByPetro(request):
    api_key = 'AIzaSyAhb8hmRYw-2idZ4kzgnbXyUw5TawiGKvA'
    result = {}
    data = json.loads(request.body)

    if data['loc_query']:
        search = GoogleMapClient(api_key=api_key,location_query=data['loc_query'])
        result['petro'] = search.search_nearby(keyword='Cay xang',radius=1000)
        result['place'] = search.get_detail()

    else:
        search = GoogleMapClient(api_key=api_key,lat=data['lat'],lng=data['lng'])
        result['petro'] = search.search_nearby(keyword='Cay xang',radius=1000)
        result['place'] = search.get_detail_by_latlng()

    return JsonResponse(result,json_dumps_params={'indent': 2})
