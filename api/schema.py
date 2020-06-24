import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from api.models import AutoMLJob
from k8s.pod_querier import PodQuerier
from k8s.pod_stopper import PodStopper
from k8s.util import JobStatus
from k8s.pod_starter import KubernetesAutoMLJob


class AutoMLType(DjangoObjectType):
    class Meta:
        model = AutoMLJob
        filter_fields = ['id']
        interfaces = (relay.Node,)
        convert_choices_to_enum = False


class StatusEnum(graphene.Enum):
    SUCCESS = 1
    FAILED = 0


class JobQuery(ObjectType):
    job = relay.Node.Field(AutoMLType)
    user_jobs = DjangoFilterConnectionField(AutoMLType)

    @classmethod
    @login_required
    def resolve_user_jobs(cls, root, info, **kwargs):
        user = info.context.user
        jobs = AutoMLJob.objects.all().filter(user=user)
        for job in jobs:
            if job.status in {JobStatus.WAITING, JobStatus.RUNNING}:
                if job.pod_name is None:
                    job.delete()
                    continue
                job.status = PodQuerier(job.pod_name).query_status_update(job.status)
                job.save()
        return AutoMLJob.objects.all().filter(user=user)


class CreateAutoMLJob(graphene.Mutation):
    class Arguments:
        input_topic = graphene.String(required=True)
        output_topic = graphene.String(required=True)
        target_column = graphene.Int(required=True)
        job_name = graphene.String(required=True)

    job = graphene.Field(AutoMLType)

    @classmethod
    @login_required
    def mutate(cls, root, info, input_topic, output_topic, target_column, job_name):
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
                                       job_name=job_name,
                                       status=JobStatus.WAITING.value,
                                       )
        kube_job.start_pod()
        job.pod_name = kube_job.pod_name
        job.save()
        return CreateAutoMLJob(job=job)


class StopAutoMLJob(graphene.Mutation):
    class Arguments:
        job_id = graphene.String(required=True)

    job = graphene.Field(AutoMLType)

    @classmethod
    @login_required
    def mutate(cls, root, info, job_id):
        user = info.context.user
        job = AutoMLJob.objects.all().get(
            user=user,
            id=from_global_id(job_id)[1]
        )
        PodStopper(job.pod_name).stop_pod()
        job.status = JobStatus.STOPPED
        job.save()
        return StopAutoMLJob(job=job)


class DeleteAutoMLJob(graphene.Mutation):
    class Arguments:
        job_id = graphene.String(required=True)

    status = StatusEnum()
    info = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, job_id):
        user = info.context.user
        job = AutoMLJob.objects.all().get(
            user=user,
            id=from_global_id(job_id)[1]
        )
        stop_status = PodStopper(job.pod_name).stop_pod()
        job.delete()
        if stop_status == "FAILED":
            return DeleteAutoMLJob(status=StatusEnum.FAILED, info="Pod not found on cluster, model has been deleted")
        return DeleteAutoMLJob(status=StatusEnum.SUCCESS, info="Pod and model succesfully deleted")


class JobMutation(object):
    create_automl_job = CreateAutoMLJob.Field()
    stop_automl_job = StopAutoMLJob.Field()
    delete_automl_job = DeleteAutoMLJob.Field()


query_list = [JobQuery]
mutation_list = [JobMutation]
