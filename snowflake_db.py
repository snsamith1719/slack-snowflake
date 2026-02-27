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

        password = generate_password()

        cur.execute(f"""
        CREATE USER IF NOT EXISTS {username}
        PASSWORD='{password}'
        DEFAULT_ROLE={role}
        DEFAULT_WAREHOUSE=COMPUTE_WH
        """)

        cur.execute(
            f"GRANT ROLE {role} TO USER {username}"
        )

        return f"✅ User {username} onboarded with role {role}"

    except Exception as e:

        return str(e)


def reset_password(username):

    conn = get_connection()
    cur = conn.cursor()

    password = generate_password()

    cur.execute(
        f"ALTER USER {username} SET PASSWORD='{password}'"
    )

    return f"✅ Password reset for {username}. Temp password: {password}"