import os
import uvicorn
import psycopg
from fastapi import FastAPI, Response
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


app = FastAPI()

@app.get("/count/{username}/{category}")
def increment_counter(category: str, username: str):

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO counters
                (username, category, count)
                VALUES (%s, %s, 1)

                ON CONFLICT (username, category)
                DO UPDATE
                SET count = counters.count + 1

                RETURNING count;
                """,
                (username, category)
            )

            count = cur.fetchone()[0]

        conn.commit()

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="180"
         height="28"
         viewBox="0 0 180 28"
         role="img"
         aria-label="Profile Views: {count}">

        <rect width="180" height="28" rx="5" fill="#555"/>

        <rect x="110" width="70" height="28" rx="5" fill="#007ec6"/>

        <text x="55" y="14"
              fill="#fff"
              font-family="Arial, sans-serif"
              font-size="12"
              text-anchor="middle"
              dominant-baseline="middle">
            Profile Views
        </text>

        <text x="145" y="14"
              fill="#fff"
              font-family="Arial, sans-serif"
              font-size="12"
              font-weight="600"
              text-anchor="middle"
              dominant-baseline="middle">
            {count}
        </text>

    </svg>
    """

    return Response(
        content=svg,
        media_type="image/svg+xml"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


