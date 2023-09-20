import os
from datetime import datetime
from typing import List, Any, Union, Tuple
from pathlib import Path
from evtx import PyEvtxParser


# instead of parsing and displaying the entire log, review suspicious event IDs or commonly known IDs and output those.
# give an option to allow for the parsing of the entire data
# https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES/tree/master
# adapted from https://github.com/omerbenamram/pyevtx-rs

def evtx_parser(file_name: str, timestamp_start="", timestamp_end="") -> Union[
        tuple[list[Any], list[ValueError]], list[Any]]:
    try:

        # Get the directory of the current Python script
        script_dir = os.path.dirname(os.path.abspath("evtx"))

        # Construct the relative path to the evtx folder
        evtx_dir = os.path.join(script_dir, "evtx")

        # Construct the full path to the evtx file
        full_path = os.path.join(evtx_dir, file_name)
        print(full_path)

        parser = PyEvtxParser(full_path, number_of_threads=0)

        event_data = []
        preserved_error_data = []
        if timestamp_start is not "":
            timestamp_start = datetime.strptime(timestamp_start, "%Y-%m-%d %H:%M:%S.%f")
        if timestamp_end is not "":
            timestamp_end = datetime.strptime(timestamp_end, "%Y-%m-%d %H:%M:%S.%f")

        for record in parser.records_json():
            try:
                record_timestamp_str = record.get("timestamp", "")
                if record_timestamp_str:
                    record_timestamp = datetime.strptime(record_timestamp_str, "%Y-%m-%d %H:%M:%S.%f %Z")

                    if (timestamp_start is "" or timestamp_end is "") or (
                            (timestamp_start is not "" and timestamp_end is not "") and
                            (timestamp_start <= record_timestamp <= timestamp_end)):
                        event_data.append(record['data'])
            except ValueError as e:
                print(f"Error parsing record: {e}")
                preserved_error_data.append(e)
        return event_data, preserved_error_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
