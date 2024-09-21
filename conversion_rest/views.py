from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def same(request):
    return Response(1)


@api_view(['GET'])
def GBP_USD(request):
    return Response(1.27)


@api_view(['GET'])
def GBP_Euro(request):
    return Response(1.17)


@api_view(['GET'])
def USD_GBP(request):
    return Response(0.79)


@api_view(['GET'])
def USD_Euro(request):
    return Response(0.92)


@api_view(['GET'])
def Euro_GBP(request):
    return Response(0.86)


@api_view(['GET'])
def Euro_USD(request):
    return Response(1.09)
