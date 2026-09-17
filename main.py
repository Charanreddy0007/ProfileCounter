from fastapi import FastAPI
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


app = FastAPI()

@app.get("/count/{name}")
def increment_counter(name: str):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO counters 
                (name, count)
                VALUES (%s, 1)
                ON CONFLICT (name)
                DO UPDATE SET count = counters.count + 1
                RETURNING count;
                """,
                (name, )
            )

            count = cur.fetchone()[0]

        conn.commit()

    return {
        "name": name,
        "count": count
    }
    


