from django.conf.urls import url
from django.urls import path
from graphene_django.views import GraphQLView

from api import views

urlpatterns = [
    url('graphql', GraphQLView.as_view(graphiql=True)),
    path('', views.test_page)
]
