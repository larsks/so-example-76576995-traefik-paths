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

## Running the tests

The [`tests/`](tests/) directory contains a simple test implemented using [pytest][]. You can run the tests like this:

1. Set the `REQUESTS_FORCE_ADDRESS` environment variable to the IP address of your ingress router. This allows URLs containing `dev.mywebsite.io` to work even if that hostname doesn't resolve or resolves to an inappropriate address. E.g., for my local environment:

    ```
    export REQUESTS_FORCE_ADDRESS=192.168.1.201
    ```

2. Run `pytest -v`.

This should result in:

```
============================= test session starts ==============================
platform linux -- Python 3.11.4, pytest-7.2.2, pluggy-1.0.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/lars/projects/kubework/traefik-middlewares
collecting ... collected 12 items

tests/test_urls.py::test_urls[http://dev.mywebsite.io/api-server-api-server-/] PASSED [  8%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/api-server/a/b/c-api-server-/a/b/c] PASSED [ 16%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/-theia-/] PASSED   [ 25%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes-hermes-/] PASSED [ 33%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes/-hermes-/] PASSED [ 41%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes/a/b/c-hermes-/a/b/c] PASSED [ 50%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2-hermes-/] PASSED [ 58%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2/-hermes-/] PASSED [ 66%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2/a/b/c-hermes-/a/b/c] PASSED [ 75%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3-hermes-/] PASSED [ 83%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3/-hermes-/] PASSED [ 91%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3/a/b/c-hermes-/a/b/c] PASSED [100%]

============================== 12 passed in 0.08s ==============================
```

[pytest]: https://docs.pytest.org/
