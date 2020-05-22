import json
import psycopg2
from contextlib import closing
from threading import Thread
from time import sleep

_payload = {"blah": "fasel"}


def cleanup():
    print("Cleanup thread started...")
    while True:
        sleep(1)
        with closing(psycopg2.connect(database="stream", user="postgres")) as conn:
            conn.autocommit=False
            with conn, conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM stream WHERE ts <= (transaction_timestamp() - interval '600 seconds')")
                conn.commit()
                print("Cleanup")
        

ct = Thread(target=cleanup)
ct.setDaemon(True)
ct.start()

print("Payload injector started...")
with closing(psycopg2.connect(database="stream", user="postgres", password="postgres")) as conn:
    conn.autocommit=False
    with conn, conn.cursor() as cur:
        while True:
            cur.execute(
                "INSERT INTO stream (payload) VALUES (%s::jsonb)", (json.dumps(_payload),))
            conn.commit()
