from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data_engine.fetchers import get_weather_data
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

        try:
            daily_df = get_weather_data(float(lat), float(lon))
            results = calculate_suitability_scores(daily_df)

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
