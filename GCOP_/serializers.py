from rest_framework import serializers
from .models import QrCodes

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCodes
        fields = ['id', 'code_data', 'scanned_at']
