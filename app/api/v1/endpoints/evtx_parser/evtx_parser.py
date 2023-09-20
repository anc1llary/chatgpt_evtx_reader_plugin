import json
from typing import List, Any, Optional

from fastapi import HTTPException
from fastapi import APIRouter
from app.services.evtx_parser.evtx_parser import evtx_parser

router = APIRouter()


@router.post("/evtx-parser",
             description="Reads, parses, and presents EVTX files as JSON data located in evtx folder.")
async def evtx_parser_api(file_name: str, timestamp_start, timestamp_end) -> list[Any]:
    try:

        event_data = evtx_parser(file_name, timestamp_start, timestamp_end)

        return event_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

