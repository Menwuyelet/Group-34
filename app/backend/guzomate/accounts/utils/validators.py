from rest_framework import serializers

def validate_picture(value):
    if value == None:
        return value
    max_size = 5 * 1024 * 1024  # 5MB
    if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
        raise serializers.ValidationError("Only JPEG, PNG, and GIF images are allowed.")
    if value.size > max_size:
        raise serializers.ValidationError("Image size should not exceed 5MB.")
    return value