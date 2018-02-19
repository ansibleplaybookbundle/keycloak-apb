# Keycloak APB

[![License](https://img.shields.io/:license-Apache2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

![keycloak image](./docs/imgs/keycloak_logo.png)

## Overview

This APB aims to deploy Keycloak on OpenShift and allow any application to provide Single Sign-On capabilities. In case an existing Keycloak instance exists somewhere else (even outside of OpenShift) this APB will allow configuring applications to connect to it.

For an overview of what each task does, please check the [APB overview file](./docs/apb_overview.md).

## Requirements
- [apb](https://github.com/fusor/ansible-playbook-bundle/blob/master/README.md#installing-the-apb-tool)

## Usage

**NOTE**: Make sure your Ansible Service Broker is running with the property `launch_apb_on_bind: true`

In the Openshift control panel, find and select the `Keycloak (APB)` and fill in the required fields.

### Plans

**Common configuration**

* **admin_username**: Name of the username that will have the administrator role in Keycloak
* **admin_password**: Password to authenticate the administrator user
* **keycloak_uri**: URL accessible from the browser where the client application should redirect users for authentication. This URL should also be reachable from the application pod as it will be used to validate the token.
* **keycloak_users**: Pre-provisioned users and role bindings
* **keycloak_roles**: Pre-provisioned roles

**Ephemeral**

Allows you to deploy a Keycloak server with a pre-provisioned Realm with the name of the `namespace`. No persistence is configured, therefore once the application is restarted, all the provisioned data will be lost. **Not suitable for production**

**Persistent**

Allows you to deploy a Keycloak server with a pre-provisioned Realm with the name of the `namespace`. A **Postgresql** instance will also be deployed and configured so that configuration is not lost upon restarts.

Additional variable:

* **pvc_size**: Size of the Persistent Volume Claim that will be created

**External**

An existing instance of Keycloak can be used for authentication/authorization. This plan will create the Realm during provisioning so that future bindings can create the *clients*.

### Pre-provision users and roles

Users example:
```
  {
      "username" : "kermit",
      "enabled": true,
      "email" : "kermit@example",
      "firstName": "Kermit",
      "lastName": "The Frog",
      "credentials" : [
          { "type" : "password",
            "value" : "piggy" }
      ],
      "realmRoles": [ "user", "admin" ]
  },
  {
      "username" : "gonzo",
      "enabled": true,
      "email" : "gonzo@example",
      "firstName": "Gonzo",
      "lastName": "The Great",
      "credentials" : [
          { "type" : "password",
            "value" : "camilla" }
      ],
      "realmRoles": [ "user" ]
  }
```

Roles example:
```
 {
    "name": "user",
    "description": "User privileges"
  },
  {
    "name": "admin",
    "description": "Administrator privileges"
  }
```

### Bind an application

After provisioning Keycloak and deploying an application `bindings` shall be created in order to provide the application with the required environment variables or files (depending on the type of the binding).

In order to create a binding, the following variables must be provided:

* **service_name**: Name of the service that will be created in order to include it in the auth redirection.
* **redirect_uris**: URL to which redirect upon authentication.

After the binding is created, the following variables are defined:

* **SSO_URL**: Keycloak URL
* **SSO_REALM**: Name of the realm within Keycloak. i.e. the `namespace`
* **SSO_CLIENT**: Name of the client provisioned. i.e. `namespace-application_name`

With this, the secret can be added to an application as environment variables or as a volume.

## Testing

An example application can be deployed as follows:
```
$ oc new-app https://raw.githubusercontent.com/ruromero/quickstarts/master/springboot-keycloak/springboot-keycloak-template.yaml
```

Once deployed, it won't become ready as the readinessProbe will fail. It will be required to create the binding providing the redirect uri and service name.

E.g. `http://springboot-myproject.example.com/*` and `springboot`

Finally, after the secret is created, you will be able to _Add to application_ as environment variables. This change triggers a new deployment and it will be possible to navigate to `/` for the public URL and to `/private` where the authentication page is prompted.

For more information about the test application check [springboot-keycloak quickstart](https://github.com/ruromero/quickstarts/tree/master/springboot-keycloak)

For more information about testing of APBs, check [ansible-playbook-bundle documentation](https://github.com/ansibleplaybookbundle/ansible-playbook-bundle/blob/master/docs/getting_started.md#test).
