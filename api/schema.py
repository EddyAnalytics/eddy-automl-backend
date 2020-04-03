import graphene
from graphene import ObjectType, String, Schema


class Query(ObjectType):
    pass


class Mutations(ObjectType):
    pass

    class StartAutoML(graphene.Mutation):
        class Arguments:
            input_topic = graphene.String()
            output_topic = graphene.String()


schema = Schema(query=Query, mutation=Mutations)
