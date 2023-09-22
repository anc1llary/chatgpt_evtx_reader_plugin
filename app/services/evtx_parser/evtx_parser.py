import os
import json
from datetime import datetime
from typing import List, Any, Union, Tuple
from pathlib import Path
from evtx import PyEvtxParser


# instead of parsing and displaying the entire log, review suspicious event IDs or commonly known IDs and output those.
# give an option to allow for the parsing of the entire data
# https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES/tree/master
# adapted from https://github.com/omerbenamram/pyevtx-rs
# fix the formatting of the output data to pretty json
# add support for multiple files

event_codes = {
    "Windows Event ID 4624 - Successful logon": 4624,
    "Windows Event ID 4625 - Failed logon attempt": 4625,
    "Windows Event ID 4634 - User logoff": 4634,
    "Windows Event ID 4648 - New logon session created": 4648,
    "Windows Event ID 4688 - New process creation": 4688,
    "Sysmon Event ID 1 - Process creation": 1,
    "Sysmon Event ID 3 - Network connection": 3,
    "Sysmon Event ID 7 - Image loaded": 7,
    "Sysmon Event ID 8 - CreateRemoteThread": 8,
    "PowerShell Module Logging (Event ID 4103) - PowerShell module loaded": 4103,
    "PowerShell ScriptBlock Logging (Event ID 4104) - PowerShell script block executed": 4104,
    "PowerShell Transcription (Event ID 400) - PowerShell session transcript": 400,
    "Security Log Event ID 4689 - Process termination": 4689,
    "Security Log Event ID 4697 - Service creation": 4697,
    "Security Log Event ID 4702 - User rights altered": 4702
}

def evtx_parser(file_name: str, timestamp_start="", timestamp_end="", known_event_ids=False):
    try:

        script_dir = os.path.dirname(os.path.abspath("evtx"))
        evtx_dir = os.path.join(script_dir, "evtx")
        full_path = os.path.join(evtx_dir, file_name)

        parser = PyEvtxParser(full_path, number_of_threads=0)

        event_data = []
        preserved_error_data = []
        if timestamp_start != "":
            timestamp_start = datetime.strptime(timestamp_start, "%Y-%m-%d %H:%M:%S.%f")
        if timestamp_end != "":
            try:
                timestamp_end = datetime.strptime(timestamp_end, "%Y-%m-%d %H:%M:%S.%f %Z")
            except ValueError as e:
                print(f"Error: {e}")
                timestamp_end = ""

        for record in parser.records_json():
            try:
                record_timestamp_str = record.get("timestamp", "")
                if record_timestamp_str:
                    record_timestamp = datetime.strptime(record_timestamp_str, "%Y-%m-%d %H:%M:%S.%f %Z")

                    if (timestamp_start is "" or timestamp_end is "") or (
                            (timestamp_start != "" and timestamp_end != "") and
                            (timestamp_start <= record_timestamp <= timestamp_end)):
                        
                        #record_data = record['data']
                        #record_data_json = json.loads(record_data)

                        #print(record_data_json['data']['EventID'])

                        ## issues grabbing [EventID] for some reason, likely because it is a mapper for a rust program...

                        # if known_event_ids == True:
                        #    for event_id in event_codes.items():
                        #        if record['data'] in event_id:
                        #            event_data.append(record['data'])
                        #            print(event_data)
                        #            print(known_event_ids)
                        #    else:      
                        event_data.append(record['data'])
            except ValueError as e:
                print(f"Error parsing record: {e}")
                preserved_error_data.append(e)
        return event_data, preserved_error_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
