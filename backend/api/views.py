from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data_engine.fetcher import get_weather_data
from data_engine.scoring import calculate_suitability_scores


# Create your views here.
class SuitabilityScoreView(APIView):
    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude data are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
