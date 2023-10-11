
# AI Ateliers

This repo is the main API of AI Atelier. It allows Clients (our mobile applications and web app) to interact with our product. 

To work properly, the API acts as a middle-tier API and fetch data from our users' emails providers (Gmail and Outlook mainly).

## Main components

This API is a FastAPI python API. After launching your app locally you can access the API documentation at the `http://localhost:8000/docs` url.

FastAPI is a very lightweight framework to manage a python API. It comes with a lot of coroutines features (`async` mode) that we could capitalized on to better manage `I/O` (with the Microsoft/Gmail API) and `CPU` use at some point with our ML models.

### Architectures

The `main.py` file is the entrypoint and contains the API endpoints. 
All the business logic is located in the `betteremail` folder with mainly: 

- `graph.py` that allows us to manage the Microsft Graph API;
- `google.py` that will allow us to manage Gmail API;


### Install

We use `poetry` as a package managers (pretty modern tool wih more features that pip to easily manage different environments). 

#### Install poetry

```
#on Mac
curl -sSL https://install.python-poetry.org | python3 -
```

#### Install dependencies

At the root
```
poetry install
```

#### Run locally

You will need environment variables. The project comes with default and publics data to work locally. Currently, you will need to ask for the `MICROSOFT_CLIENT_SECRET` variable.

At the root
```
uvicorn main:app --reload
```


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

We use the [On-Behalf-Of](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow) workflow with matches what we want to do.

/!\ For now we have only one App registered. We could, in the future look for having 2 App registered:

- one for the client - API ;
- one the API - Graph;

This could give us more flexibility to manage scopes and rights.

## Gmail

It's a work in progress. The interface already exists though.
