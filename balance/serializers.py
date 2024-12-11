from rest_framework import serializers


class BalanceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(write_only=True)

    def update(self, instance, validated_data):
        if instance.balance - validated_data.get("amount") < 0:
            raise serializers.ValidationError({"error": "Insufficient balance"})
        instance.balance = instance.balance - validated_data.get("amount")
        instance.save()
        return instance
