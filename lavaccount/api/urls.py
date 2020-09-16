from rest_framework import routers
from .api import AccountViewSet, MasterPasswordViewSet


router = routers.DefaultRouter()
router.register('api/account', AccountViewSet, 'account')
router.register('api/masterpassword', MasterPasswordViewSet, 'masterpassword')

urlpatterns = router.urls
