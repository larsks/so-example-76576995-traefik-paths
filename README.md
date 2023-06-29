This repository accompanies [this answer on Stack Overflow][answer].

[answer]: https://stackoverflow.com/a/76584818/147356

## To Deploy

This repository is designed to be deployed using Kustomize. You can deploy it like this:

```
kubectl apply -k .
```

Note that when referencing Middlewares, Traefik requires the name to be prefixed with the Namespace. I'm deploying these into a Namespace named `example`, so we see:

```
  annotations:
    traefik.ingress.kubernetes.io/router.middlewares: example-add-trailing-slash@kubernetescrd
```

If you are deploying this into any other namespace, you will need to edit the above annotation to replace `example` with the appropriate name.
