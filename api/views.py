from django.http import HttpResponse
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

import os

# Create your views here.
def test_page(request):

    # Use API token if passed as env variable
    K8S_API_KEY = os.environ.get('K8S_API_KEY')
    if K8S_API_KEY:
        configuration = client.Configuration()
        configuration.api_key['authorization'] = K8S_API_KEY
        api_client = client.BatchV1Api(client.ApiClient(configuration))
    else:
        try:
            config.load_incluster_config()
        except ConfigException:
            config.load_kube_config()

        api_client = client.BatchV1Api()

    core_api_client = client.CoreV1Api()
    print('Listing pods with their IPs:')
    ret = core_api_client.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print('%s\t%s\t%s' %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    apps_api_client = client.AppsV1Api()
    container = client.V1Container(
        name="nginx",
        image="nginx:1.15.4",
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {'app': 'nginx'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name='test-ngnix-3' ),
        spec=spec)

    api_response = apps_api_client.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))

    return HttpResponse("Deployment created. status='%s'" % str(api_response.status))
