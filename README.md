
# AI Ateliers

This repo is the main API of AI Atelier. It allows Clients (our mobile applications and web app) to interact with our product. 

To work properly, the API acts as a middle-tier API and fetch data from our users' emails providers (Gmail and Outlook mainly).

## Main components

This API is a FastAPI python API. After launching your app locally you can access the API documentation at the `http://localhost:8000/docs` url.


## Workflow

- A user who first tries to interact to our API will be asked to provide his email;
- Based on the email, we will require the user to complete an oAuth2 workflow, and consent to our requirements (access to their inbox on their behalf);
- Then, the client can start interacting with the API which will act on behalf of our users to fetch data from their mail boxes directly;

## Identity providers

## Microsoft

This is for users with `@outlook.fr` or `@microsoft.com` email addresses.

### Set up

We have registered an App on Azure AD `betteremail-mobile-client`.
with the following scopes: 

- profile, email, openid, offline_access, Mail.Read
- Mail.read

We use the [On-Behalf-Of](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow) workflow.


## Gmail

It's a work in progress. The interface already exists though.
