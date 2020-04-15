from k8s.util import PodOperator, namespace, JobStatus


class PodStopper(PodOperator):
    def __init__(self, pod_name):
        super().__init__()
        self.pod_name = pod_name

    def stop_pod(self):
        self.client.delete_namespaced_pod(
            name=self.pod_name,
            namespace=namespace
        )
        return JobStatus.STOPPED
