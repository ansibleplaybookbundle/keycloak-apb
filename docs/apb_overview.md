# Overview

This document outlines the steps for each APB task to help people  understand what is happening under the hood.

# Provision

## Persistent
Create a new Postgres service, including:
  * Secrets for database admin users
  * Service for the Postgres DB
  * PersistVolume Claim to for the Postgres DB
  * DeploymentConfig for the Postgres DB

## Persistent + Ephemeral
Create a new Keycloak service, including:
  * DeploymentConfig for Keycloak
    * Link Keycloak and Postgres DB
    * Add default Keycloak admin user credential
  * Service for Keycloak
  * Route HTTPS for Keycloak

## Persistent + Ephemeral + External
Create a new realm in Keycloak using the current OpenShift project name and display name

# Bind

* Create a new client with the provided service and redirect_uri in Keycloak. It is created in the realm that matches the current namespace.
* Persist the newly created client name and password as `_apb_bind_creds`

# Unbind

* Delete the client from Keycloak

# Deprovision

## Ephemeral and Persistent
1. Delete all the routes
  * Keycloak
2. Delete all the services
  * Keycloak
  * Postgres
3. Delete all the deploymentConfigs
  * Keycloak
  * Postgres
4. Delete all the secrets
  * Postgres
5. Delete all the persistent volume claims
  * Postgres
6. Delete all the imageStreams
  * Keycloak

## External
* Delete the realm
