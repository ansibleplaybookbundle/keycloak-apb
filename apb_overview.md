# Overview

This document outlines the steps for each APB task to help people to understand what is happening under the hood.

# Provision

1. Create a new Postgres service, including:
    * Secrets for database admin users
    * Service for the Postgres DB
    * PersistVolume Claim to for the Postgres DB
    * DeploymentConfig for the Postgres DB
2. Create a new Keycloak service, including:
    * DeploymentConfig for Keycloak
        * Link Keycloak and Postgres DB
        * Add default Keycloak admin user credential
    * Service for Keycloak
    * Route HTTPS for Keycloak
    * Create a new realm in Keycloak using the current OpenShift project name

# Bind

1. Create a new client with the provided service and redirect_uri in Keycloak. It is created in the realm that matches the current namespace.
2. Persist the newly created client name and password as `_apb_bind_creds`

# Unbind

1. Delete the client from Keycloak

# Deprovision

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
