from django.conf.urls import url
from graphene_django.views import GraphQLView

urlpatterns = [
    url('graphql', GraphQLView.as_view(graphiql=True)),
]
