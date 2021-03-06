# Konfplate

A docker image aimed to be used as an initContainer in Kubernetes to facilitate configuration templating.

It is considered good pratice to build application containers with embedded configuration templating.
However, this may be both *time consuming* and *not needed* while using a container orchestration solution.

Kubernetes proposes a simple way to launch a processus before your real application / container / pod is started, which is named *InitContainers*.

This docker image is a perfect option to use *InitContainers* as a configuration template renderer.

## In details

Konfplate currently exists in two flavors: the first one is implemented in Python and uses the
[jinja2](http://jinja.pocoo.org/) template engine and the second one is implemented in Go and uses its
[standard template engine](https://golang.org/pkg/text/template/).

The image take 5 kinds of parameters as an input :
- a single configuration template file (written in jinja2)
- a location (a path) to push the rendered configuration
- an optional comma separated list of secrets or values to load through environment
- an optional comma separated list of secrets or values to load through files
- an optional comma separated list of objects, represented in JSON, to load through files

## How to use

Here is the usage for the Python version:

```
usage: konfplate [-h] [-t TEMPLATE] [-o OUTPUT] [-e ENV_VAR] [-f FILE_PATH]
                 [-j JSON_PATH] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        A configuration template
  -o OUTPUT, --output OUTPUT
                        A path to write the rendered configuration to
  -e ENV_VAR, --env ENV_VAR
                        One or more environment variable to load (default:
                        load the complete environment)
  -f FILE_PATH, --file FILE_PATH
                        One or more file to load as text
  -j JSON_PATH, --json JSON_PATH
                        One or more JSON file to load as an object each
  -d, --debug           Enable debug mode
```

And here is the usage for the Go version:

```
Usage of konfplate:
  -d, --debug             Enable debug mode
  -e, --env strings       One or more environment variable to load (default: load the complete environment)
  -f, --file strings      One or more file to load as text
  -j, --json strings      One or more JSON file to load as an object each
  -o, --output string     A path to write the rendered configuration to (default "-")
  -t, --template string   A configuration template (default "-")
```

As you can see, the usage of both tool is pretty similar so you can easily interchange them.

To choose between the two flavors, use the docker image tags. For example for the latest version of the tool:

- enix/konfplate:jinja-latest
- enix/konfplate:gotpl-latest

The complete list of tags is available on the [docker hub](https://hub.docker.com/r/enix/konfplate/tags).

## Kubernetes spec
Here is a typical spec to use konfplate:
```
apiVersion: v1
kind: Pod
metadata:
  name: testpod
  labels:
    app: testpod
spec:
  initContainers:
  - name: config-template
    image: enix/konfplate:jinja-2
    command:
      - ./konfplate
      - --template=/templates/test.conf.jinja
      - --output=/rendered/test.conf
      - --env=PATH
      - --file=/templates/test.file
      - --json=/templates/test.json
    volumeMounts:
    - name: config-template-volume
      mountPath: /templates
    - name: config-rendered-volume
      mountPath: /rendered
  containers:
  - name: testpod
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
    volumeMounts:
    - name: config-rendered-volume
      mountPath: /etc/config/
  volumes:
    - name: config-template-volume
      configMap:
        name: config-template
    - name: config-rendered-volume
      emptyDir: {}
```
it is based on a configMap:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-template
data:
  test.conf.jinja: |-
    This is a configuration template used for test purposes.
    It will render a typical env value >{{ env.PATH }}<,
    a file >{{ file.test_file }}<,
    a json file >{{ json.test_json.name }}<,
    and finally a missing value >{{ dummy }}<
  test.file: a value extracted from a file
  test.json: |-
    {
      "name": "a name extracted from a json file"
    }
```
Both these specs are available [here](manifests/container-with-templated-configuration.pod.yaml).

In an ideal setup, Kubernetes secrets would be loaded through files and loaded with the `--file` flag and the template would not be in the same configMap.

You might also want to have more than one *InitContainer* in order to render several configuration files.

## Troubleshoot
The logs of the *InitContainer* are available though the usual kubectl command line:
`kubectl logs <pod_name> -c konfplate`

## Todo
- implement a HashiCorp Vault client in order to mix local and vault based secrets

# License
Copyright (c) ENIX S.A.S. Corporation. All rights reserved.

Licensed under the [MIT License](LICENSE).

# Credits
A bit thanks to the [envplate](https://github.com/kreuzwerker/envplate) project which helped a lot in building simple to use containers.
