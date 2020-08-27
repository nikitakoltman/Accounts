from rest_framework import serializers
from .models import Account, MasterPassword


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = '__all__'

class MasterPasswordSerializer(serializers.ModelSerializer):
	class Meta:
		model = MasterPassword
		fields = '__all__'