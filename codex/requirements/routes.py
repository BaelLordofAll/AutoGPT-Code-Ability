import logging
from typing import Optional
from fastapi import APIRouter, FastAPI, Path, Query, Request, Response, UploadFile
import json

import codex.database
from codex.api_model import (
    Indentifiers,
    SpecificationResponse,
    SpecificationsListResponse,
)
from codex.requirements.agent import generate_requirements

logger = logging.getLogger(__name__)

spec_router = APIRouter()


# Specs endpoints


@spec_router.post(
    "/user/{user_id}/apps/{app_id}/specs/",
    tags=["specs"],
    response_model=SpecificationResponse,
)
async def create_spec(user_id: int, app_id: int, description: str):
    """
    Create a new specification for a given application and user.
    """
    try:
        app = await codex.database.get_app_by_id(user_id, app_id)
        ids = Indentifiers(user_id=user_id, app_id=app_id)

        spec = generate_requirements(ids, app.name, description)
        return SpecificationResponse.from_specification(spec)
    except Exception as e:
        return Response(
            content=json.dumps(
                {"error": f"Error creating a new specification: {str(e)}"}
            ),
            status_code=500,
            media_type="application/json",
        )


@spec_router.get(
    "/user/{user_id}/apps/{app_id}/specs/{spec_id}",
    response_model=SpecificationResponse,
    tags=["specs"],
)
async def get_spec(user_id: int, app_id: int, spec_id: int):
    """
    Retrieve a specific specification by its ID for a given application and user.
    """
    try:
        specification = await codex.database.get_specification(user_id, app_id, spec_id)
        if specification:
            return specification
        else:
            return Response(
                content=json.dumps({"error": "Specification not found"}),
                status_code=500,
                media_type="application/json",
            )
    except Exception as e:
        logger.error(f"Error retrieving specification: {e}")
        return Response(
            content=json.dumps({"error": "Error retrieving specification"}),
            status_code=500,
            media_type="application/json",
        )


@spec_router.put(
    "/user/{user_id}/apps/{app_id}/specs/{spec_id}",
    response_model=SpecificationResponse,
    tags=["specs"],
)
async def update_spec(
    user_id: int,
    app_id: int,
    spec_id: int,
    spec_update: SpecificationResponse,
):
    """
    TODO: This needs to be implemented
    Update a specific specification by its ID for a given application and user.
    """
    return Response(
        content=json.dumps(
            {"error": "Updating a specification is not yet implemented."}
        ),
        status_code=500,
        media_type="application/json",
    )


@spec_router.delete("/user/{user_id}/apps/{app_id}/specs/{spec_id}", tags=["specs"])
async def delete_spec(user_id: int, app_id: int, spec_id: int):
    """
    Delete a specific specification by its ID for a given application and user.
    """
    try:
        await codex.database.delete_specification(spec_id)
        return Response(
            content=json.dumps({"message": "Specification deleted successfully"}),
            status_code=200,
            media_type="application/json",
        )
    except Exception as e:
        logger.error(f"Error deleting specification: {e}")
        return Response(
            content=json.dumps({"error": "Error deleting specification"}),
            status_code=500,
            media_type="application/json",
        )


@spec_router.get(
    "/user/{user_id}/apps/{app_id}/specs/",
    response_model=SpecificationsListResponse,
    tags=["specs"],
)
async def list_specs(
    user_id: int,
    app_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    """
    List all specifications for a given application and user.
    """
    try:
        specs = await codex.database.list_specifications(
            user_id, app_id, page, page_size
        )
        return specs
    except Exception as e:
        logger.error(f"Error listing specifications: {e}")
        return Response(
            content=json.dumps({"error": "Error listing specifications"}),
            status_code=500,
            media_type="application/json",
        )
