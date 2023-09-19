import os
from http.client import HTTPException

from evtx import PyEvtxParser


# adapted from https://github.com/omerbenamram/pyevtx-rs
def evtx_parser(evtx_path: str) -> None:


    parser = PyEvtxParser("/mnt/c/tmp/test.evtx", number_of_threads=0)


    for record in parser.records_json():
        print("lol2")
        print(f'Event Record ID: {record["event_record_id"]}')
        print(f'Event Timestamp: {record["timestamp"]}')
        print(record['data'])
        print('------------------------------------------')

