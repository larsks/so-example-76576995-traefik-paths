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
tests/test_urls.py::test_urls[http://dev.mywebsite.io/api-server-api-server] PASSED              [  7%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/-theia] PASSED                             [ 15%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes-hermes] PASSED                      [ 23%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes/-hermes] PASSED                     [ 30%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes/foo-theia] PASSED                   [ 38%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2-hermes] PASSED                     [ 46%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2/-hermes] PASSED                    [ 53%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes2/foo-theia] PASSED                  [ 61%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3-hermes] PASSED                     [ 69%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3/-hermes] PASSED                    [ 76%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes3/foo-hermes] PASSED                 [ 84%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes113-theia] PASSED                    [ 92%]
tests/test_urls.py::test_urls[http://dev.mywebsite.io/hermes_was_a_dog-theia] PASSED             [100%]
```

[pytest]: https://docs.pytest.org/
