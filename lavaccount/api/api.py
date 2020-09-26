from rest_framework import viewsets, permissions

from .models import Account, MasterPassword
from .serializers import AccountSerializer, MasterPasswordSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """docstring for ClassName"""
    queryset = Account.objects.all()
    permissions_classes = [
        permissions
    ]
    serializer_class = AccountSerializer


class MasterPasswordViewSet(viewsets.ModelViewSet):
    """docstring for ClassName"""
    queryset = MasterPassword.objects.all()
    permissions_classes = [
        permissions
    ]
    serializer_class = MasterPasswordSerializer
