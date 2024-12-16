from rest_framework import serializers

def change_balance(user, amount):
    if amount < 0 and user.balance + amount < 0:
        raise serializers.ValidationError({"error": "Insufficient balance"})
    user.balance += amount
    user.save()
    return user


class BalanceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(write_only=True)

    def update(self, instance, validated_data):
        amount = validated_data.get("amount")
        change_balance(instance, amount)
        return instance
