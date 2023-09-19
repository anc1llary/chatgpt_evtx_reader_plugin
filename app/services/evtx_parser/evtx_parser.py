from evtx import PyEvtxParser

# adapted from https://github.com/omerbenamram/pyevtx-rs
def evtx_parser(evtx_path: str) -> None:

    parser = PyEvtxParser(evtx_path)

    for record in parser.records_json():
        print(f'Event Record ID: {record["event_record_id"]}')
        print(f'Event Timestamp: {record["timestamp"]}')
        print(record['data'])
        print('------------------------------------------')
