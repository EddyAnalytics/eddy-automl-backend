import graphene
from graphene import ObjectType, String, Schema
from graphene_django import DjangoObjectType

from api.models import AutoMLJob


class AutoMLType(DjangoObjectType):
    class Meta:
        model = AutoMLJob


class CreateAutoMLJob(graphene.Mutation):
    class Arguments:
        input_topic = graphene.String(required=True)
        output_topic = graphene.String(required=True)
        target_column = graphene.String(required=True)

    job = graphene.Field(AutoMLType)

    def mutate(self, info, input_topic, output_topic, target_column):
        user = info.context.user
        job = AutoMLJob.objects.create(user=user,
                                       input_topic=input_topic,
                                       output_topic=output_topic,
                                       target_column=target_column)
        job.save()
        return CreateAutoMLJob(job=job)


class Queries(ObjectType):
    jobs = graphene.List(AutoMLType)

    def resolve_jobs(self, info):
        user = info.context.user
        return AutoMLJob.objects.all().filter(user=user)


class Mutations(ObjectType):
    CreateAutoMLJob = CreateAutoMLJob.Field()


schema = Schema(query=Queries, mutation=Mutations)
