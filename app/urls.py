from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    url('graphql', jwt_cookie(GraphQLView.as_view(graphiql=True))),
    path('admin', admin.site.urls),
    path("api", include('api.urls')),
    path("authentication", include('authentication.urls'))
]
