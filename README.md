# Eddy AutoML - Backend

> Eddy AutoML is an automated machine learning platform for streaming data. Part of the Eddy Analytics Platform.

Backend API service for Eddy AutoML. Used for scheduling, managing and monitoring AutoML jobs.

## Development Setup

Enable permissive RBAC for the development cluster:
```
kubectl create clusterrolebinding permissive-binding \
  --clusterrole=cluster-admin \
  --user=admin \
  --user=kubelet \
  --group=system:serviceaccounts
````

RBAC Docs: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

```bash
devspace dev
```

