from kubernetes.client.rest import ApiException

from k8s.util import PodOperator, namespace


class PodStopper(PodOperator):
    def __init__(self, pod_name):
        super().__init__()
        self.pod_name = pod_name

    def stop_pod(self) -> str:
        try:
            self.client.delete_namespaced_pod(
                name=self.pod_name,
                namespace=namespace
            )
        except ApiException:
            return "FAILED"
        return "SUCCESS"
