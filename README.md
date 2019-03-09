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