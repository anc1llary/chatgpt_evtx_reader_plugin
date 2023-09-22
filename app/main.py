import tomli
import yaml
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from string import Template
from fastapi import Request, Response
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints.evtx_parser.evtx_parser import router as evtx_parser_router
import os

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path
file_path = os.path.join(parent_dir, '../pyproject.toml')

# Load the TOML file
with open(file_path, mode="rb") as fp:
    config = tomli.load(fp)

__version__ = config["tool"]["poetry"]["version"]
DESCRIPTION = config["tool"]["poetry"]["description"]
TITLE = config["app"]["title"]
PLUGIN_HOSTNAME = config["app"]["plugin_hostname"]

main_app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=__version__
)
# Enable CORS
origins = [
    "http://localhost:9001",
    "https://chat.openai.com",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(evtx_parser_router, prefix="/api/v1/evtx")

main_app.mount("/static", StaticFiles(directory="static"), name="static")

main_app.mount("/evtx", StaticFiles(directory="evtx"), name="evtx")


# Set up required files in .well-known directory/
@main_app.get("/.well-known/ai-plugin.json", include_in_schema=False, description="Serves the ai-plugin.json file to chatgpt.")
async def get_ai_plugin(request: Request) -> Response:
    """
    Serve the ai-plugin.json file.

    This function reads the ai-plugin.json file, replaces string placeholders with their actual values,
    and then serves the modified content as a plain text response.

    Parameters:
    request (Request): The incoming HTTP request object.

    Returns:
    Response: A FastAPI Response object containing the modified ai-plugin.json content.

    """

    with open(os.path.join(parent_dir, "../ai-plugin.json"), "r") as f:
        content_str = f.read()

    content_str = Template(content_str).safe_substitute(PLUGIN_HOSTNAME=PLUGIN_HOSTNAME)

    return Response(content=content_str, media_type="text/plain")


@main_app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml(request: Request) -> Response:
    """
    Serve the openapi.yaml file.

    Parameters:
    request (Request): The incoming HTTP request object.

    Returns:
    Response: A FastAPI Response object containing the modified OpenAPI schema in YAML format.

    """

    openapi_data = main_app.openapi()

    openapi_data["info"]["servers"] = [PLUGIN_HOSTNAME]

    openapi_yaml = yaml.dump(openapi_data)

    with open('../openapi.yaml', 'w') as file:
        file.write(openapi_yaml)

    return Response(content=openapi_yaml, media_type="text/plain")


def start():
    print(f"{TITLE} v{__version__} - {DESCRIPTION}")
    uvicorn.run("app.main:main_app", host="0.0.0.0", port=9001, reload=True)
