
# AI Ateliers

This repo is the main API of AI Atelier. It allows Clients (our mobile applications and web app) to interact with our product. 

To work properly, the API acts as a middle-tier API and fetch data from our users' emails providers (Gmail and Outlook mainly).

## Main components

This API is a FastAPI python API. After launching your app locally you can access the API documentation at the `http://localhost:8000/docs` url.

FastAPI is a very lightweight framework to manage a python API. It comes with a lot of coroutines features (`async` mode) that we could capitalized on to better manage `I/O` (with the Microsoft/Gmail API) and `CPU` use at some point with our ML models.

## Local development

The `main.py` file is the entrypoint and contains the API endpoints. 
All the business logic is located in the `betteremail` folder with mainly: 

- `graph.py` that allows us to manage the Microsft Graph API;
- `google.py` that will allow us to manage Gmail API;


### Install

We use `poetry` as a package managers (pretty modern tool wih more features that pip to easily manage different environments). 

### Install poetry

```
#on Mac
curl -sSL https://install.python-poetry.org | python3 -
```

### Install dependencies

At the root
```
poetry install
```

### Run locally

You will need environment variables. The project comes with default and publics data to work locally. Currently, you will need to ask for the `MICROSOFT_CLIENT_SECRET` variable.

At the root
```
uvicorn main:app --reload
```

/!\ To test the main endpoints you'll have to provide the Access Token. This token is obtained when the user SignIn with its provider. It's recommended to use a simple SPA or Postman workflow to get the Access Token.

### Launch the tests

```
poetry run pytest
```

### Deploy

The platform used for deployment is heroku. As heroku doesn't handle `poetry` well, one has to make sure the `requirements.txt` file is up to date by running the following command before a new deployment: 

```
poetry export -f requirements.txt --output requirements.txt
```

This will allow heroku to use the `pip` package manager for the deployment.

## Workflow

- A user who first tries to interact to our API will be asked to provide his email;
- Based on the email, we will require the user to complete an oAuth2 workflow, and consent to our requirements (access to their inbox on their behalf);
- At this point the client should have i) an access token ii) an id token;
- The client can start interacting with the API which will act on behalf of our users to fetch data from their mail boxes directly;

For example if the client wants to know if there is a new email waiting for the user in the inbox: 

```
{root_url}/emails?since=2023-10-11T13:20:59Z&idToken={IdToken}
```

TODO: For now the access token isn't used but should be provided (as an Authorisation header) and verify for each private endpoints.

## Authorisations between Client & our API

For now we only check the IdToken. We also should verify the access token the user got in the same oauth2 workflow.

## Identity providers

## Microsoft

This is for users with `@outlook.fr` or `@microsoft.com` email addresses.

### Set up

We have registered an App on Azure AD `betteremail-mobile-client`.
with the following scopes: 

- profile, email, openid, offline_access, Mail.Read
- Mail.read

We use the [On-Behalf-Of](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow) workflow with matches what we want to do.

/!\ For now we have only one App registered. We could, in the future look for having 2 App registered:

- one for the client - API ;
- one the API - Graph;

This could give us more flexibility to manage scopes and rights.

## Gmail

It's a work in progress. The interface already exists though.
