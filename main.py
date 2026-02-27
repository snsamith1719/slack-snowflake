from fastapi import FastAPI, Form
from snowflake_db import onboard_user, reset_password
from auth import is_authorized
from fastapi import FastAPI, Form, BackgroundTasks
import requests



app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


app = FastAPI()


def process_command(text, response_url):

    args = text.split()

    action = args[0]

    if action == "reset_password":

        username = args[1]

        result = reset_password(username)

    elif action == "onboard_user":

        username = args[1]
        role = args[2]

        result = onboard_user(username, role)

    else:

        result = "Invalid command"

    requests.post(
        response_url,
        json={"text": result}
    )

@app.post("/slack-command")
async def slack_command(
    background_tasks: BackgroundTasks,
    user_id: str = Form(...),
    text: str = Form(...),
    response_url: str = Form(...)
):

    if not is_authorized(user_id):
        return {"text": "❌ Unauthorized"}

    background_tasks.add_task(
        process_command,
        text,
        response_url
    )

    return {"text": "⏳ Processing..."}

@app.post("/slack-command")
async def slack_command(
    user_id: str = Form(...),
    text: str = Form(...)
):

    if not is_authorized(user_id):
        return {"text": "❌ Unauthorized"}

    args = text.split()

    if len(args) == 0:
        return {"text": "Invalid command"}

    action = args[0]

    if action == "onboard_user":

        if len(args) < 3:
            return {"text":"Usage: onboard_user <username> <role>"}

        username = args[1]
        role = args[2]

        result = onboard_user(username, role)

        return {"text": result}


    elif action == "reset_password":

        if len(args) < 2:
            return {"text":"Usage: reset_password <username>"}

        username = args[1]

        result = reset_password(username)

        return {"text": result}


    return {"text": "Invalid command"}