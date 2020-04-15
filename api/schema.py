import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from api.models import AutoMLJob
from k8s.pod_querier import PodQuerier
from k8s.util import JobStatus
from k8s.job_submission import KubernetesAutoMLJob


class AutoMLType(DjangoObjectType):
    class Meta:
        model = AutoMLJob
        filter_fields = ['id']
        interfaces = (relay.Node,)
        convert_choices_to_enum = False


class JobQuery(ObjectType):
    job = relay.Node.Field(AutoMLType)
    user_jobs = DjangoFilterConnectionField(AutoMLType)

    @classmethod
    @login_required
    def resolve_user_jobs(cls, root, info, **kwargs):
        user = info.context.user
        return AutoMLJob.objects.all().filter(user=user)


class CreateAutoMLJob(graphene.Mutation):
    class Arguments:
        input_topic = graphene.String(required=True)
        output_topic = graphene.String(required=True)
        target_column = graphene.Int(required=True)
        name = graphene.String(required=True)

    job = graphene.Field(AutoMLType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input_topic, output_topic, target_column, name):
        user = info.context.user
        kube_job = KubernetesAutoMLJob(
            input_topic=input_topic,
            output_topic=output_topic,
            target_col=target_column
        )
        job = AutoMLJob.objects.create(user=user,
                                       input_topic=input_topic,
                                       output_topic=output_topic,
                                       target_column=target_column,
                                       job_name=name,
                                       status=JobStatus.WAITING.value
                                       )  # TODO edit such that it reflects actual job state
        kube_job.start_pod()
        job.pod_name = kube_job.pod_name
        job.status = PodQuerier(kube_job.pod_name).query_status_update(job.status).value
        job.save()
        return CreateAutoMLJob(job=job)


class JobMutation(object):
    create_automl_job = CreateAutoMLJob.Field()


query_list = [JobQuery]
mutation_list = [JobMutation]
