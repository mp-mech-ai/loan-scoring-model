---
title: "Loan Scoring Model"
emoji: "💰"
colorFrom: "red"
colorTo: "yellow"
sdk: "docker"
sdk_version: "29.1.4"
app_file: "src/api/main.py"
pinned: false
---

# Loan Scoring Model

This project presents an API that uses a machine learning model to score loan applications, and a Web Application that allows users to interact with the API and monitor the model's performance and drift.

# Installation
You will need to get few services in order to use this project. They are free but needs some configuration.

## Logging API request

Create an account on [BetterStack](https://betterstack.com/):
- Create a project and a source
- Retrieve the token and the host
- Store them in `.env` as `LOGTAIL_TOKEN` and `LOGTAIL_HOST` (with "https//") and in Github Secrets
- Now [create an API Token for this source](https://betterstack.com/docs/warehouse/querying-data/ad-hoc-sql-api/)
- And store the username, the password and the host as `BETTERSTACK_USERNAME`, `BETTERSTACK_PASSWORD` and `BETTERSTACK_HOST` in `.env`

The logs should look like this:
![BetterStack Logs](assets/betterstack-log.png)

## Deploying Locally

This project uses Docker to build and run the API and Web Application. To install Docker, follow the instructions on the [Docker website](https://www.docker.com/get-started/).

Then at the root of the project, run:
`docker compose build && docker compose up --env-file .env`

Then `.env` should contain the following variables:

- `LOGTAIL_TOKEN`,
- `LOGTAIL_HOST`,
- `BETTERSTACK_USERNAME`,
- `BETTERSTACK_PASSWORD`,
- `BETTERSTACK_HOST`,
- `API_BASE_URL=http://api:8000`

You can then access the API at `http://localhost:8000`, and the Web Application at `http://localhost:8050`.


# Web Application

The Web Application allows you two things:
- In the `Demo` tab, you can query the API to retrieve the information of a specific client (based on its `SK_ID_CURR`) and see what score the model predicts for this client,
![alt text](assets/webapp-demo.png)

- In the `Analytics` tab, you can see :
    - An Evidently Drift Report,
    - The API usage over the past day,
    - The score distribution predicted by the API over the past day,
    - The live API latency (refreshed every 5 seconds).

![alt text](assets/webapp-analytics.png)

# API

The API is a FastAPI application that uses a machine learning model to score loan applications. The API is deployed on Docker and the doc can be accessed at `http://api:8000/doc`.