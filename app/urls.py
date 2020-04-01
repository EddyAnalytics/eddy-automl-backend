from django.urls import path, include
from graphene_django.views import GraphQLView

urlpatterns = [
    path("api", include('api.urls')),
]
