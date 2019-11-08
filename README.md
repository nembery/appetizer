# APP-ITIZER

Appitzier is a simple docker container that can create an app from any Skillet or repository of Skillets. 


## Getting started
 
Set an environment variable that points to your Skillet repository (or a comma separated list of them)

```bash

export appetizer_REPO=https://github.com/PaloAltoNetworks/iron-skillet.git

```

Then create the container with the docker run command:

```bash

docker run -p 8080:8080 paloaltonetworks/appitzier:latest

```


Browse to localhost and enjoy your new app!
