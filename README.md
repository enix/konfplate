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
FIXME pod spec with init container

`configtemplate --template <configuration_template> --output <rendered_configuration> --envs <env1>,<env2>,... --files <file1>,<file2>,... --jsons <json_file1>,<json_file2>,...`

