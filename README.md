# APPETIZER

Appetzier is a simple docker container that can create a standalone app from any repository containing Skillets. 


## Getting started
 
Set an environment variable that points to your Skillet repository (or a comma separated list of them)

```bash

export REPO=https://github.com/PaloAltoNetworks/iron-skillet.git
export BRANCH='panos_v9.0'

```

Then create the container with the docker run command:

```bash

docker run -p 8080:8080 -t registry.gitlab.com/panw-gse/as/appetizer

```

Or, all in one command such as:

```bash

docker run -it --rm -p 8088:8080 -e 'REPO=https://github.com/PaloAltoNetworks/SkilletBuilder.git' \
  -e 'BRANCH=develop' \ 
  --name "Skillet Builder" registry.gitlab.com/panw-gse/as/appetizer

```

Browse to localhost and enjoy your new app!
