from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path("api", GraphQLView.as_view(graphiql=True)),
    # path("", "landing page woot")
]
