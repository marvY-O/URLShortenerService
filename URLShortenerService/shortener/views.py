from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import URL
from .serializer import db_serializer, short_url_response_serializer
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
import validators
import time
from .convertor import Convertor

dId = 1
mId = 1

def generate(dID, mID):
    """
    Generates a Unique ID (64bit Integer)
    """

    timens = time.time_ns()

    signedBit = 0
    datacenterID = dID
    timestamp = int(timens/pow(10,6))
    machineID = mID
    sequenceID = timens%pow(10,6)//4096

    signedBit = format(signedBit,'b').rjust(1, "0")
    timestamp = format(timestamp,'b').rjust(41, "0")
    datacenterID = format(datacenterID, 'b').rjust(5, "0")
    machineID = format(machineID,'b').rjust(5, "0")
    sequenceID = format(sequenceID, 'b').rjust(12, "0")

    uid = signedBit + timestamp + datacenterID + machineID + sequenceID

    uid = int(uid, 2)

    return uid


class short_url_response:
    def __init__(self, short_url):
        self.short_url = short_url


# Create your views here.
@api_view(['POST'])
def shorten(request):
    """
    Shortens the given long url
    """
    #begin_time = time.time()

    data = request.data
    if ("long_url" not in data):
        return Response("long_url not found!", status = status.HTTP_400_BAD_REQUEST)
    if (not validators.url(data["long_url"])):
        return Response("invalid URL!", status = status.HTTP_400_BAD_REQUEST)
    
    #db_time = 0
    
    #db_begin = time.time()
    entry = URL.objects.filter(long_url = data["long_url"])

    #db_time += time.time() - db_begin

    if (entry.exists()):
        surl = short_url_response(entry.values()[0]["short_url"])
        serializer = short_url_response_serializer(surl)

        #print("Already exists: {}ms".format((time.time()-begin_time)*1000))
        #print("Db access: {}ms".format(db_time*1000))
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    newURL = URL()
    newURL.uid = generate(dId, mId)
    newURL.long_url = data["long_url"]
    newURL.short_url = Convertor.int_to_base62(newURL.uid)

    #db_begin = time.time()
    newURL.save()

    #db_time += time.time() - db_begin

    surl = short_url_response(newURL.short_url)
    serializer = short_url_response_serializer(surl)

    #print("Created: {}ms".format((time.time()-begin_time)*1000))
    #print("Db access: {}ms".format(db_time*1000))

    return Response(serializer.data, status = status.HTTP_200_OK)

class retrieve_url_test(APIView):
    def get(self, request, shortID):
        #time_begin = time.time()
        uid = Convertor.base62_to_int(shortID)
        product = URL.objects.filter(uid=uid)

        if (not product.exists()):
            #print("Retrieve time: {}ms".format((time.time() - time_begin)*1000))
            return Response("Invalid!", status = status.HTTP_400_BAD_REQUEST)
        
        #print("Retrieve time: {}ms".format((time.time() - time_begin)*1000))
        return Response(product.values()[0]["long_url"], status=200)


class retrieve_url(APIView):
    def get(self, request, shortID):
        #time_begin = time.time()
        uid = Convertor.base62_to_int(shortID)
        product = URL.objects.filter(uid=uid)

        if (not product.exists()):
            #print("Retrieve time: {}ms".format((time.time() - time_begin)*1000))
            return Response("Invalid!", status = status.HTTP_400_BAD_REQUEST)
        
        #print("Retrieve time: {}ms".format((time.time() - time_begin)*1000))
        return HttpResponseRedirect(redirect_to=product.values()[0]["long_url"])
