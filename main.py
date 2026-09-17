import os
import uvicorn
import psycopg
from fastapi import FastAPI
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


