import graphene
import graphql_jwt

import api.schema
import authentication.schema

RootQuery = type(
    'RootQuery',
    tuple(
        authentication.schema.query_list +
        api.schema.query_list
    ),
    {}
)

RootMutation = type(
    'RootMutation',
    tuple(
        authentication.schema.mutation_list +
        api.schema.mutation_list
    ),
    {}
)


class Query(RootQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(RootMutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project

    # auth mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # delete_refresh_token_cookie = graphql_jwt.refresh_token.DeleteRefreshTokenCookie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
