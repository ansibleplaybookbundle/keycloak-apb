# Keycloak APB

[![](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)](https://hub.docker.com/r/aerogearcatalog/keycloak-apb/)
[![Docker Stars](https://img.shields.io/docker/stars/aerogearcatalog/keycloak-apb.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/aerogearcatalog/keycloak-apb/stars/count/)
[![Docker pulls](https://img.shields.io/docker/pulls/aerogearcatalog/keycloak-apb.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/aerogearcatalog/keycloak-apb/)
[![License](https://img.shields.io/:license-Apache2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

## Overview

For an overview of what each task does, please check the [APB overview file](./apb_overview.md).

## Requirements
- [apb](https://github.com/fusor/ansible-playbook-bundle/blob/master/README.md#installing-the-apb-tool)

**NOTE:**
Due to our usage of an older version of the ASB, it is recommended using the `apb` CLI like the following:

```bash
alias apb='docker run --rm --privileged -v $PWD:/mnt -v $HOME/.kube:/.kube -v /var/run/docker.sock:/var/run/docker.sock -u $UID docker.io/ansibleplaybookbundle/apb-tools:latest'
```

Instead of the `abp` alias, you might want to use a modified alias, such as `apb-fh`, to not conflict w/ other versions that might be installed already on your machine.

## Testing

To test changes made locally, after making the changes, run:

```bash
make apb_build DOCKERORG="<defaulting to aerogearcatalog>" DOCKERHOST="<defaulting to docker.io>"`
```

If changes were made to the `apb.yml` file, then you will need to execute `apb bootstrap` (if this fails, then you can also run the `~/repos/catasb/local/<os>/reset_environment.sh`), though this takes a little while. Changes to the APB ansible files do not require the above step.

In the Openshift control panel, find and select the `Keycloak (APB)` and fill in the required fields.

You can also test new changes by running `apb test`. What this command does in general is described in [metrics-apb readme](https://github.com/aerogearcatalog/metrics-apb#testing).

For more information about testing of APBs, check [ansible-playbook-bundle documentation](https://github.com/ansibleplaybookbundle/ansible-playbook-bundle/blob/master/docs/getting_started.md#test).

## Publish

To publish the changes, you can run:

```bash
make DOCKERORG="<defaulting to aerogearcatalog>" DOCKERHOST="<defaulting to docker.io>"
```

Make sure you have the permission to push images to the docker org.
