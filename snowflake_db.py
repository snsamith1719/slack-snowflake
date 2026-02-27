import snowflake.connector
import os


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

        cur.execute(
            f"CREATE USER {username} PASSWORD='Temp123!'"
        )

        cur.execute(
            f"GRANT ROLE {role} TO USER {username}"
        )

        return f"✅ User {username} onboarded"

    except Exception as e:

        return str(e)



def reset_password(username):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            f"ALTER USER {username} SET PASSWORD='Temp123!'"
        )

        return f"✅ Password reset for {username}"

    except Exception as e:

        return str(e)