from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from finances.api.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = User.objects.all().select_related('profile')
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


# class ProfileForm(viewsets.ModelViewSet):
#     """
#     API endpoint for ProfileForm.
#     """
#     queryset = Profile.objects.all().order_by('-date_joined')


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
