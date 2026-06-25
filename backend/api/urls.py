from django.urls import path
from api.views import SuitabilityScoreView

urlpatterns = [
    path("score/", SuitabilityScoreView.as_view(), name="score_api"),
]
