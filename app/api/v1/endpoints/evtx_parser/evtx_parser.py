import json

from fastapi import HTTPException
from fastapi import APIRouter
from app.services.evtx_parser.evtx_parser import evtx_parser

router = APIRouter()


@router.post("/evtx-parser",
             description="Parses EVTX files provided by the user.")
async def evtx_parser_api(directory: str) -> None:
    try:
        print(directory)
        evtx_parser(directory)
        #return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

