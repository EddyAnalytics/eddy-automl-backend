import os

from kubernetes import config, client

namespace = os.environ.get("NAMESPACE")


def create_pod_object():
    config.load_incluster_config()
    container = client.V1Container(
        name="eddy-automl",
        image="eddyanalytics/eddy-automl",
        ports=[client.V1ContainerPort(container_port=8888)])
    spec = client.V1PodSpec(containers=[container])
    metadata = client.V1ObjectMeta(
        generate_name="automl-",
        namespace=namespace
    )
    # Instantiate the deployment object
    pod = client.V1Pod(
        kind="Pod",
        spec=spec,
        metadata=metadata
    )
    return pod


def create_pod(api_instance, pod):
    api_response = api_instance.create_namespaced_pod(
        body=pod,
        namespace=namespace)
    print("Deployment created. status='%s'" % str(api_response.status))


def execute_autoMLJob():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    pod = create_pod_object()
    create_pod(v1, pod)
