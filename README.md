# Order-User Microservice Project

## Overview

This is a microservices-based system featuring User and Order services. It follows a client-server architecture where the server is deployed on Google Cloud Platform (GCP), and the API Gateway is hosted locally to act as the entry point for the client.

The application architecture supports scalability and modular service deployment, making it suitable for real-world distributed systems.

## Project Structure

![image](https://github.com/user-attachments/assets/c7df875c-2561-4459-8be3-ba95afb63130)


## Architecture

**Microservices:** 

Modular separation between order and user components.

API Gateway: Acts as a centralized router for client requests, hosted locally.

**Deployment:**

Server-side components (user/order services) are deployed on GCP.

The client communicates through the API gateway for service discovery and routing.

Strangler Pattern: The system uses the strangler fig pattern for incremental migration and versioning. This is reflected in the presence of both user-service-v1 and user-service-v2, enabling safe evolution and refactoring of services without disrupting existing clients.
