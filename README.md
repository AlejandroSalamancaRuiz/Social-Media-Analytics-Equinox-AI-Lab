# Project - Alejandro Salamanca

This repository contains the final project of AI-Enabled Systems.

The project is intended as a tool for social media analytics. It focuses on analyzing LinkedIn posts and followers of the company Equinox AI & Data Lab https://www.linkedin.com/company/equinox-ai-lab. 

The tool's objective is to answer some relevant questions about the network of followers and content published by the company.

## Architecture

The application's architecture is thought so the backend and frontend can be decoupled and deployed in different containers or VMs. 

![Architecture](Architecture.png "Architecture")

The backend is responsible for: 
- Connecting to the Azure Cosmos DB (MongoDB) where the LinkedIn information is stored.
- Storing the specific information of content and followers in a graph inside a Neo4j database.
- Querying the Neo4j Database.
- Exposing results of queries as REST services with Flask.


The frontend is responsible for:
- Making the HTTP requests to the backend server.
- Deploying the results in a dashboard with the streamlit framework.

In the config file is the URL to connect to the Cosmos DB.

## Assumptions and restrictions

For this application to work, some assumptions need to be considered.

All the packages in the requirements.txt file need to be installed.
Although the application was built to decouple the frontend and backend, the current implementation is built to run locally.
Neo4j is already installed, and the default database 'neo4j' will be used to create the graph and make the queries.
The connection to the Neo4j database needs to be changed in the config file for the application to work.
For streamlit to work correctly, run the command pip install -U click==8

