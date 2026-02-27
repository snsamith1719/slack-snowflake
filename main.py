from fastapi import FastAPI, Form
from snowflake_db import onboard_user, reset_password
from auth import is_authorized

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


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