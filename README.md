# Config Template

A docker image aimed to be used as an initContainer in Kubernetes to facilitate configuration templating

It is considered good pratice to build application containers with embedded configuration templating.

However, this may be both *time consuming* and *not needed* while using a container orchestration solution.

Kubernetes proposes a simple way to launch a processus before your real application / container / pod is started, which is named *InitContainers*.

This docker image is a perfect option to use *InitContainers* as configuration template renderer.

## in details

It is implemented in Python and uses the [jinga2](http://jinja.pocoo.org/) template engine.
*It might also be available as go template version in the future based on community feedback*

The image take 5 kinds of parameters as an input :
- a single configuration template file (written in jinga2)
- a location (a path) to push the rendered configuration
- an optional comma separated list of secrets or values to load through environment
- an optional comma separated list of secrets or values to load through files
- an optional comma separated list of objects, represented in JSON, to load through files

## how to use
```
usage: config-template.py [-h] -t TEMPLATE -o OUTPUT [-e ENV_VAR]
                          [-f FILE_PATH] [-j JSON_PATH]
                          [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        A configuration template
  -o OUTPUT, --output OUTPUT
                        A path to write the rendered configuration to
  -e ENV_VAR, --env ENV_VAR
                        One or more environment variable to load
  -f FILE_PATH, --file FILE_PATH
                        One or more file to load as text
  -j JSON_PATH, --json JSON_PATH
                        One or more JSON file to load as an object each
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level, default: WARNING
  --version             show program's version number and exit

The complete environment will be loaded by default. To limit to specific
environment variables use the --env flag.
```

## kubernetes spec
Here is a typical spec to use config-template:
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
    image: docker-registry.enix.io/docker/config-template/master:0e246491966e1c8bcdfc24e1bf1d410dccf293f9
    command:
      - ./config-template.py
      - --template=/templates/test.conf.template
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
  imagePullSecrets:
  - name: enix
```
it is based on a configMap:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-template
data:
  test.conf.template: |-
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

## todo
- implement a the go templating language
- implement a HashiCorp Vault client in order to mix local and vault based secrets