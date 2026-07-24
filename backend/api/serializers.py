from rest_framework import serializers


class SuitabilityQuerySerializer(serializers.Serializer):
    lat = serializers.FloatField(
        min_value=-90.0, max_value=90.0, help_text="Latitude (-90.0 to 90.0)"
    )
    lon = serializers.FloatField(
        min_value=-180.0, max_value=180.0, help_text="Longitude (-180.0 to 180.0)"
    )
