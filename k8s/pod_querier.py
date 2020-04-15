from kubernetes import config, client

from k8s.util import namespace, JobStatus


class PodQuerier:
    def __init__(self, pod_name: str):
        config.load_incluster_config()
        self.client = client.CoreV1Api()
        self.pod_name = pod_name

    def query_status_update(self, curr_status: JobStatus) -> JobStatus:
        response = self.client.read_namespaced_pod_status(
            namespace=namespace,
            name=self.pod_name
        )
        state_object = response.status.container_statuses[0].state
        if state_object.running is not None:
            return JobStatus.RUNNING
        elif state_object.terminated is not None:
            if curr_status in {JobStatus.RUNNING, JobStatus.WAITING, JobStatus.FAILED}:
                return JobStatus.FAILED
            else:
                return JobStatus.STOPPED
        elif state_object.waiting is not None:
            if curr_status == JobStatus.RUNNING:
                return JobStatus.FAILED
            else:
                return curr_status
