from django.urls import include, path
from rest_framework import routers
from finances.api.views import UserViewSet, GroupViewSet
from finances.views import CreateTransactionAPIView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('transactions/create/', CreateTransactionAPIView.as_view(),
         name='create_transaction_api'),

    # path('transactions/create/<int:pk>/', CreateTransactionAPIView.as_view(),
    #      name='create_transaction_api'),


]


