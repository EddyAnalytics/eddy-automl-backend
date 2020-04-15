from kubernetes import config, client
from kubernetes.client import V1EnvVar

from k8s.util import namespace, kafka_address, PodOperator


class KubernetesAutoMLJob(PodOperator):

    def __init__(self, input_topic: str, output_topic: str, target_col: int):
        super().__init__()
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.target_col = target_col
        self.pod_name = None

    def create_pod_object(self):
        config.load_incluster_config()
        container = client.V1Container(
            name="eddy-automl",
            image="eddyanalytics/eddy-automl",
            ports=[client.V1ContainerPort(container_port=8888)],
            env=[V1EnvVar("BOOTSTRAP_SERVER", kafka_address)],
            command=["python", "main.py"],
            args=[self.input_topic, self.output_topic, str(self.target_col)]
        )
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

    def start_pod(self):
        pod = self.create_pod_object()
        api_response = self.client.create_namespaced_pod(
            body=pod,
            namespace=namespace)
        self.pod_name = api_response.metadata.name
        return api_response
