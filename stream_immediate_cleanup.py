import json
import psycopg2
from contextlib import closing
from time import sleep

_payload = {"blah": "fasel"}

print("Payload injector started...")
with closing(psycopg2.connect(database="stream", user="postgres")) as conn:
    conn.autocommit=False
    with conn, conn.cursor() as cur:
        while True:
            cur.execute(
                "INSERT INTO stream (payload) VALUES (%s::jsonb); DELETE FROM stream WHERE ts <= (transaction_timestamp() - interval '600 seconds')", (json.dumps(_payload),))
            conn.commit()
            
