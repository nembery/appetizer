# APPETIZER

Appetzier is a simple docker container that can create an app from any Skillet or repository of Skillets. 


## Getting started
 
Set an environment variable that points to your Skillet repository (or a comma separated list of them)

```bash

export REPO=https://github.com/PaloAltoNetworks/iron-skillet.git
export BRANCH='panos_v9.0'

```

Then create the container with the docker run command:

```bash

docker run -p 8080:8080 -t nembery/appitzier

```

Or, all in one command such as:

```bash

docker run -e 'REPO=https://github.com/PaloAltoNetworks/GPCSskillets.git' -e 'BRANCH=develop' -p 8088:8080 --rm -t nembery/appetizer

```



Browse to localhost and enjoy your new app!
