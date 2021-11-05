from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer

from urllib.parse import urlencode
import requests
# Create your views here.

geolocate_data={}
def extract_lat_lng(address):
    endpoint='https://maps.googleapis.com/maps/api/geocode/json'
    key=''
    params={"address":address,'key':key}
    url_params=urlencode(params)
    url=f"{endpoint}?{url_params}"
    r=requests.get(url)
    if r.json()['status']!='OK':
        return 91,91
    lat_lng=r.json()['results'][0]['geometry']['location']
    return lat_lng['lat'],lat_lng['lng']


def address_to_geo(data):
    global geolocate_data

    lat,lng=extract_lat_lng(data['address'])
    if lat==91:
        geolocate_data["coordinates"]={"lat":0.0,'lng':0.0}
        geolocate_data['address']="Enter valid address"
    else:
        geolocate_data["coordinates"]={"lat":lat,'lng':lng}
        geolocate_data['address']=data['address']        
    return geolocate_data

def index(request):
    return render(request,'index.html')

class LocationView(APIView):
    
    renderer_classes = [JSONRenderer]
    def get(self,request,*args,**kwargs):
        data={
            'message': 'Nothing to show here use post request',
        }
        return Response(data)

    def post(self,request,*args,**kwargs):
        self.renderer_classes = [JSONRenderer, ]
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            geolocate_data=address_to_geo(request.data)
            output_format=request.data['output_format']
            if output_format.lower()=='json':
                return Response(geolocate_data)
            else:
                
                return(redirect('/xml'))
        else:
            return Response(serializer.errors)

class XmlView(APIView):
    renderer_classes = [XMLRenderer]
    def get(self, request,*args,**kwargs):
        global geolocate_data
        return Response(geolocate_data)
        

#python3 manage.py drf_create_token chiru
#e61c31e3e5e27fa15e1c634207f5a507a4712c2e
