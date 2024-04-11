---
date: 2024-04-11T15:39:01.599505
author: AutoGPT <info@agpt.co>
---

# joke-api

Based on the user's preference for dad jokes due to their universal appeal and safe-to-share nature, and leveraging the found dad joke, 'Why don't eggs tell jokes? Because they'd crack each other up.', we will implement a single endpoint in a FastAPI application. This endpoint will serve a pre-selected or dynamically generated dad joke upon request. The tech stack to achieve this includes Python for the programming language, FastAPI as the API framework due to its simplicity and performance for building web APIs, PostgreSQL for the database to store jokes or user preferences if needed in the future, and Prisma as the ORM to facilitate database operations within the Python environment. This setup will ensure a robust, scalable, and easy-to-maintain web service that delivers dad jokes to users, aligning with the user's humor preferences and contributing to a light-hearted user experience.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joke-api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
