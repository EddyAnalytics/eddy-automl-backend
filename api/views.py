from django.http import HttpResponse
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

import os

# Create your views here.
def test_page(request):

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

    v1 = client.CoreV1Api()
    print('Listing pods with their IPs:')
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print('%s\t%s\t%s' %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


    return HttpResponse('test page')
