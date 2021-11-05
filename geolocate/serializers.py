from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=1000)
    output_format = serializers.CharField(max_length=50)

    def validate_output_format(self, value):

        if value.lower()!="json" and value.lower()!="xml":
            raise serializers.ValidationError("Enter valid outupt format")
        return value
