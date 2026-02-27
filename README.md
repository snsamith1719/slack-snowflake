# Slack Snowflake User Management Bot

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/snsamith1719/slack-snowflake)

This repository contains a FastAPI application that integrates with Slack as a slash command. It allows authorized Slack users to perform basic user management tasks in a Snowflake database, such as onboarding new users and resetting passwords directly from Slack.

## Features

- **Onboard User**: Create a new user in Snowflake with a specified role and a randomly generated password.
- **Reset Password**: Reset the password for an existing Snowflake user and receive a new temporary password.
- **Authorization**: Restricts command usage to a predefined list of Slack user IDs for security.

## Prerequisites

- Python 3.8+
- A Snowflake account with a user that has privileges to create users and alter passwords.
- A Slack workspace where you can configure a new slash command.

## Setup & Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/snsamith1719/slack-snowflake.git
    cd slack-snowflake
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and populate it with your Snowflake credentials and authorized Slack user IDs.

    ```dotenv
    # Snowflake Connection Details
    SNOWFLAKE_USER="your_snowflake_user"
    SNOWFLAKE_PASSWORD="your_snowflake_password"
    SNOWFLAKE_ACCOUNT="your_snowflake_account_identifier"
    SNOWFLAKE_WAREHOUSE="your_snowflake_warehouse"
    SNOWFLAKE_DATABASE="your_snowflake_database"
    SNOWFLAKE_SCHEMA="your_snowflake_schema"

    # Slack Authorization
    # Comma-separated list of Slack User IDs allowed to run commands
    AUTHORIZED_USERS="U0XXXXXXXX,U0YYYYYYYY"
    ```

4.  **Run the application:**
    Use `uvicorn` to run the FastAPI server.
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The application will be running at `http://localhost:8000`.

## Slack Configuration

1.  Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new Slack App.
2.  Navigate to the **Slash Commands** feature in the sidebar.
3.  Click **Create New Command**.
4.  Fill in the command details:
    - **Command**: e.g., `/snowflake`
    - **Request URL**: The publicly accessible URL where this application is hosted, followed by the `/slack-command` endpoint (e.g., `https://your-ngrok-url.io/slack-command`).
    - **Short Description**: A brief description of what the command does.
5.  Install the app to your workspace.

## Usage

Once the application is running and the Slack command is configured, you can use the following commands within your Slack workspace.

### Onboard a New User

Creates a new user in Snowflake and assigns them a specified role.

**Syntax:**
`/your-command onboard_user <username> <role>`

**Example:**
`/snowflake onboard_user john.doe ANALYST`

**Response in Slack:**
`✅ User john.doe onboarded with role ANALYST`

### Reset a User's Password

Resets the password for an existing Snowflake user and provides a new temporary password.

**Syntax:**
`/your-command reset_password <username>`

**Example:**
`/snowflake reset_password jane.doe`

**Response in Slack:**
`✅ Password reset for jane.doe. Temp password: <generated_password>`

### Error Handling

- If an unauthorized user attempts to use the command:
  `❌ Unauthorized`
- If the command format is incorrect:
  `Usage: onboard_user <username> <role>`
  `Usage: reset_password <username>`

## Code Overview

- `main.py`: The main FastAPI application file. It defines the `/slack-command` endpoint that receives, parses, and routes requests from Slack.
- `snowflake_db.py`: Contains all the database logic, including establishing a connection to Snowflake, creating new users, and resetting passwords. It also includes a function to generate secure, random passwords.
- `auth.py`: Handles the authorization logic by checking if the Slack `user_id` from the command request is in the `AUTHORIZED_USERS` list defined in the `.env` file.
- `requirements.txt`: A list of all the Python dependencies required to run the project.
