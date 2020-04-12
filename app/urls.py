from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

urlpatterns = [
    url('graphql', GraphQLView.as_view(graphiql=True)),
    path('admin', admin.site.urls),
    path("api", include('api.urls')),
    path("authentication", include('authentication.urls'))
]
