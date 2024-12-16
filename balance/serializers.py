from rest_framework import serializers


class BalanceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(write_only=True)

    def update(self, instance, validated_data):
        amount = validated_data.get("amount")
        if amount < 0 and instance.balance + amount < 0:
            raise serializers.ValidationError({"error": "Insufficient balance"})
        instance.balance += amount
        instance.save()
        return instance
