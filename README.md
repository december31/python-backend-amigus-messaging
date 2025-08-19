# Amigus Messaging Backend

This is the backend for the **Amigus Messaging** mobile application, built with the Django framework. This project provides a robust API for all core messaging features, user management, and social functionalities as outlined in the BFD (Basic Feature Diagram).

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

## Business Function Diagram (BFD)

The BFD below provides a high-level overview of the backend's architecture and the relationships between its key features.

![Amigus Messaging BFD](docs/bfd.svg)

<br>

***

<br>

## Getting Started

### Prerequisites
- Python 3.8+
- Django
- Django REST Framework (DRF)
- A database (e.g., PostgreSQL, MySQL)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd amigus-messaging-backend
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    - Create a `.env` file in the project root.
    - Add your database credentials, secret key, and other configurations.
    - Example:
      ```
      SECRET_KEY=your_secret_key
      DATABASE_URL=postgres://user:password@host:port/database_name
      ```
5.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

The API will now be available at `http://127.0.0.1:8000/`.
