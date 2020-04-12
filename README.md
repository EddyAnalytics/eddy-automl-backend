# Eddy AutoML - Backend

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

