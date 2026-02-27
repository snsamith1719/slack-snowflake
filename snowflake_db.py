import snowflake.connector
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

def generate_password():

    chars = string.ascii_letters + string.digits + "@#$%"

    return ''.join(random.choice(chars) for _ in range(14))


def get_connection():

    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


def onboard_user(username, role):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # Try creating user
        cur.execute(
            f"CREATE USER {username} PASSWORD='Temp123!'"
        )

        cur.execute(
            f"GRANT ROLE {role} TO USER {username}"
        )

        return f"✅ User {username} onboarded"

    except Exception as e:

        if "already exists" in str(e):

            return f"⚠️ User {username} already exists"

        return f"❌ Error: {str(e)}"


def reset_password(username):

    conn = get_connection()
    cur = conn.cursor()

    password = generate_password()

    cur.execute(
        f"ALTER USER {username} SET PASSWORD='{password}'"
    )

    return f"✅ Password reset for {username}. Temp password: {password}"