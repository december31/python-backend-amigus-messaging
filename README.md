# Amigus Messaging Backend

This is the backend for the **Amigus Messaging** mobile application, built with the Django framework. It provides a robust API for all core messaging
features, user management, and social functionalities as outlined in the BFD (Basic Feature Diagram). This project is containerized using Docker and
Docker Compose for easy setup and deployment.

<br>

***

<br>

## Key Features

The backend API supports the following core functionalities:

### 1. User Management

- **Sign up**: Allows new users to create an account.
- **Sign in**: Enables existing users to log in.
- **Forgot password**: Provides a mechanism for password recovery.
- **Change password**: Lets users update their password.
- **Profile customization**: Supports user profile updates (e.g., changing profile pictures, names, etc.).
- **Multi-device support**: Ensures a seamless experience across multiple devices for a single user account.

### 2. Messaging

- **Text message**: API endpoints for sending and receiving text messages.
- **Image/Video/Audio message**: Handles media file uploads and sharing.
- **File sharing**: Supports the sending of various file types.
- **Group chat**: Manages group creation, membership, and messaging.
- **Edit/Delete message**: Allows users to modify or remove sent messages.
- **Message encryption**: Implements a secure messaging protocol, possibly using a **hybrid approach** as noted in the diagram.

### 3. Calling

- **Voice call**: Supports one-on-one and group voice calls.
- **Video call**: Supports one-on-one and group video calls.

### 4. Notification Management

- **New message notification**: Pushes notifications for incoming messages.
- **New friend request notification**: Notifies users of new friend requests.

### 5. Story

- **Upload story**: Enables users to share temporary content (stories).
- **Remove story**: Allows users to delete their stories.
- **Watch story**: Provides an interface for viewing others' stories.
- **Story privacy**: Manages privacy settings for who can view a user's stories.

### 6. OAuth

- **Google/Facebook/Zalo integration**: Supports user authentication via popular third-party services.

<br>

***

<br>

## Basic Feature Diagram (BFD)

The BFD below provides a high-level overview of the backend's architecture and the relationships between its key features.

![Amigus Messaging BFD](docs/bfd.svg)

<br>

***

<br>

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation and Setup with Docker

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/december31/python-backend-amigus-messaging.git]
    cd python-backend-amigus-messaging
    ```
2. **Build and run the containers:**
    - Use Docker Compose to build the images and start the services (web, database, etc.).
    ```bash
    docker-compose -f compose-dev.yaml up -d --build
    ```

The API will now be available at `http://localhost:1103/`.

### Development

- The `compose-dev.yml` file is configured for development, with hot-reloading enabled for code changes.
- To create a superuser, run:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
