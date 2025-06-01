from rest_framework import serializers

class DrugLabelSerializer(serializers.Serializer):
    active_ingredient = serializers.CharField()
    dosage_form = serializers.CharField()
    purpose = serializers.CharField()

class SideEffectsSerializer(serializers.Serializer):
    drug = serializers.CharField()
    side_effects = serializers.ListField(
        child = serializers.CharField()
)