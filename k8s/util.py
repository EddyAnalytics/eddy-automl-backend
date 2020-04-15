import os
from enum import Enum

from kubernetes import config, client

namespace = os.environ.get("NAMESPACE")
kafka_address = os.environ.get("KAFKA-ADDR")


class JobStatus(Enum):
    WAITING = 0
    RUNNING = 1
    STOPPED = 2

    FAILED = -1

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class PodOperator:
    def __init__(self):
        config.load_incluster_config()
        self.client = client.CoreV1Api()
