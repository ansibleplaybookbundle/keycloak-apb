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
    * Routes (either HTTP or HTTPS depends on the option) for Keycloak
    * Create a new realm in Keycloak using the current OpenShift project name
    * Create a new public Keycloak client (with generated name and password) in the newly created realm
    * Create a new bearer-only Keycloak client with the same generated name and password in the newly created realm
    * Create a new secret in the current OpenShift namespace with the following info:
        * URL of the Keycloak service
        * Admin user credentials
        * Realm name
        * Details about the newly created public Keycloak client
        * Details about the newly created bearer-only Keycloak client
    * Persist the admin user credential as `_apb_provision_creds`
3. Create a new Keycloak-metrics service, including:
    * DeploymentConfig for Keycloak-metrics
    * Persistent volume claim for Keycloak-metrics
    * Service for Keycloak-metrics
    * Copy `keycloak-monitoring-prometheus.jar` to Keycloak to collect metrics data about Keycloak

# Bind

1. Get the Keycloak admin user token using the Keycloak admin user credential
2. Create a new bearer-only client with a newly generated name and password in Keycloak. It is created in the realm that matches the current namespace.
3. Persist the newly created client name and password as `_apb_bind_creds`

# Unbind

1. Get the Keycloak admin user token using the Keycloak admin user credential
2. Delete the client from Keycloak using the data persisted in `_apb_bind_creds`

# Deprovision

1. Delete all the routes
    * Keycloak
2. Delete all the services
    * Keycloak
    * Postgres
    * Keycloak-metrics
3. Delete all the deploymentconfigs
    * Keycloak
    * Postgres
    * Keycloak-metrics
4. Delete all the secrets
    * Keycloak
    * Postgres
5. Delete all the persistent volume claims
    * Keycloak-metrics
    * Postgres
