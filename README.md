# Nepal Cyber Resilience Platform: Technical Documentation

## 1. Introduction

Welcome to the technical documentation for the Nepal Cyber Resilience Platform. This document provides a comprehensive overview of the project, from its conceptualization and architecture to its implementation details and security measures.

The purpose of this documentation is to serve as a central guide for developers, maintainers, and stakeholders, ensuring a clear understanding of the system's components and logic.

The Nepal Cyber Resilience Platform is a web-based application designed to enhance cybersecurity awareness, facilitate incident reporting, and provide valuable resources to users in Nepal. It aims to create a centralized hub for tracking and understanding the cyber threat landscape in the region.

## 2. Project Overview

### Justification and Inspiration

The digital landscape in Nepal is rapidly expanding, bringing with it an increased risk of cyber threats to individuals, businesses, and government entities. There is a growing need for a unified platform that not only educates the public on best practices but also provides a streamlined way to report and analyze cyber incidents. This project is inspired by the goal of creating a safer digital environment for Nepali citizens by fostering a community-driven approach to cybersecurity.

### Key Features of the Application

The platform is built with a focus on usability, security, and scalability. The core features include:

*   **User Authentication:** Secure registration and login system for users, including support for social sign-on via Google for ease of access.
*   **Incident Reporting:** A structured form for users to report cybersecurity incidents, such as phishing, malware attacks, or online scams.
*   **Knowledge Base:** A repository of articles, guides, and best practices to educate users about various cybersecurity topics.
*   **User Dashboard:** A personalized space for users to track their reported incidents and access resources.
*   **Admin Panel:** A secure backend interface for administrators to manage users, review incident reports, and publish content to the knowledge base.
*   **RESTful API:** A well-documented API to support the frontend application and allow for potential future integrations.

## 3. Technology Stack

The application is built on a modern, robust, and scalable technology stack. The choice of technologies is guided by industry best practices, performance, and developer productivity.

| Category      | Technology                                                              | Description                                                                                                                              |
| :------------ | :---------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**   | **Node.js** with **Express.js**                                         | A fast, unopinionated, and minimalist web framework for Node.js, used to build the RESTful API.                                          |
|               | **Sequelize**                                                           | A promise-based Node.js ORM for Postgres, MySQL, MariaDB, SQLite, and more. It simplifies database interactions and prevents SQL injection. |
|               | **`google-auth-library`**                                               | Used for authenticating users via Google OAuth 2.0, providing a secure and convenient login option.                                      |
|               | **`jsonwebtoken`**                                                      | Implements JSON Web Tokens (JWT) for creating secure, stateless authentication sessions for API access.                                  |
|               | **`bcryptjs`**                                                          | A library to hash user passwords before storing them in the database, protecting user credentials.                                       |
|               | **`swagger-jsdoc`**                                                     | Generates OpenAPI (Swagger) documentation from JSDoc comments, ensuring the API is well-documented and easy to consume.                |
|               | **`dotenv`**                                                            | Manages environment variables, keeping sensitive data like database credentials and API keys out of the source code.                   |
| **Frontend**  | **React / Vue / Angular** (Assumed)                                     | A modern JavaScript framework for building a dynamic, responsive, and user-friendly single-page application (SPA).                     |
| **Database**  | **PostgreSQL / MySQL**                                                  | A powerful, open-source relational database system managed by Sequelize to store application data.                                     |
| **Deployment**| **Docker, Heroku, AWS, GCP**                                            | Containerization and cloud platforms for scalable and reliable deployment of the application.                                            |

## 4. Design and Architecture

The application follows a classic **Client-Server Architecture**. The system is decoupled into two main parts: a frontend client (likely a Single Page Application) and a backend server that exposes a RESTful API.

### Backend Architecture

The backend is structured using a pattern similar to **Model-View-Controller (MVC)**, adapted for an API-only service:

*   **Models:** Defined using Sequelize, these represent the database tables (`User`, `Incident`, `Article`) and contain the business logic for data manipulation.
*   **Controllers:** These handle the incoming HTTP requests, process input, interact with the models to perform database operations, and send back a response.
*   **Routes:** These map the API endpoints (e.g., `/api/incidents`) to the corresponding controller functions.
*   **Middleware:** Functions that execute before the main controller logic, used for tasks like authentication, authorization (RBAC), input validation, and logging.

## 5. Database and Backend Logic

### Database Schema

The database schema is designed to be relational and is managed by Sequelize migrations. The core models include:

*   **Users:** Stores user information, credentials, and roles.
    *   `id` (PK)
    *   `name` (STRING)
    *   `email` (STRING, UNIQUE)
    *   `passwordHash` (STRING)
    *   `googleId` (STRING, NULLABLE)
    *   `role` (ENUM: 'user', 'admin')
*   **Incidents:** Stores details of user-reported incidents.
    *   `id` (PK)
    *   `title` (STRING)
    *   `description` (TEXT)
    *   `status` (ENUM: 'reported', 'in_progress', 'resolved')
    *   `reportedBy` (FK to Users.id)
*   **Articles:** Stores content for the knowledge base.
    *   `id` (PK)
    *   `title` (STRING)
    *   `content` (TEXT)
    *   `authorId` (FK to Users.id)

### Important Code Snippets

#### Environment Configuration with `dotenv`

We use `dotenv` to load environment-specific configurations securely. This is one of the first things loaded in the application.

```javascript
// index.js
require('dotenv').config();

const express = require('express');
const app = express();

const PORT = process.env.PORT || 5000;

// Database connection
const sequelize = require('./config/database');

// ... rest of the app setup


