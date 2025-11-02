from rest_framework import serializers
from .models import MissingPerson


class MissingPersonSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    flyer_url = serializers.SerializerMethodField()
    marker_url = serializers.SerializerMethodField()
    physical_description = serializers.CharField(source='get_physical_description', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    
    class Meta:
        model = MissingPerson
        fields = [
            'id', 'name', 'age', 'gender', 'height', 'weight', 'hair_color', 'eye_color',
            'distinguishing_features', 'physical_description', 'last_seen_date',
            'last_seen_location', 'circumstances', 'contact_name', 'contact_phone',
            'contact_email', 'police_case_number', 'police_department', 'photo_url',
            'flyer_url', 'marker_url', 'upload_date', 'last_updated', 'owner_name',
        ]
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None
    
    def get_flyer_url(self, obj):
        request = self.context.get('request')
        if obj.digital_flyer and request:
            return request.build_absolute_uri(obj.digital_flyer.url)
        return None
    
    def get_marker_url(self, obj):
        request = self.context.get('request')
        if obj.ar_marker_image and request:
            return request.build_absolute_uri(obj.ar_marker_image.url)
        elif obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None