import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.get_joke_service
import project.get_preferences_service
import project.login_service
import project.refresh_token_service
import project.submit_feedback_service
import project.update_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joke-api",
    lifespan=lifespan,
    description="Based on the user's preference for dad jokes due to their universal appeal and safe-to-share nature, and leveraging the found dad joke, 'Why don't eggs tell jokes? Because they'd crack each other up.', we will implement a single endpoint in a FastAPI application. This endpoint will serve a pre-selected or dynamically generated dad joke upon request. The tech stack to achieve this includes Python for the programming language, FastAPI as the API framework due to its simplicity and performance for building web APIs, PostgreSQL for the database to store jokes or user preferences if needed in the future, and Prisma as the ORM to facilitate database operations within the Python environment. This setup will ensure a robust, scalable, and easy-to-maintain web service that delivers dad jokes to users, aligning with the user's humor preferences and contributing to a light-hearted user experience.",
)


@app.post(
    "/feedback", response_model=project.submit_feedback_service.SubmitFeedbackResponse
)
async def api_post_submit_feedback(
    userId: str, feedbackContent: str, feedbackType: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Allows users to submit feedback about the app or the jokes.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            userId, feedbackContent, feedbackType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/joke", response_model=project.get_joke_service.JokeResponse)
async def api_get_get_joke(
    preference: Optional[str],
) -> project.get_joke_service.JokeResponse | Response:
    """
    Serves a dad joke either randomly or based on the user's preferences.
    """
    try:
        res = await project.get_joke_service.get_joke(preference)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/preferences",
    response_model=project.get_preferences_service.GetPreferencesResponse,
)
async def api_get_get_preferences() -> project.get_preferences_service.GetPreferencesResponse | Response:
    """
    Retrieves the logged-in user's set preferences.
    """
    try:
        res = await project.get_preferences_service.get_preferences()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    email: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Endpoint for user login, returning a JWT token upon successful authentication.
    """
    try:
        res = await project.login_service.login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/preferences/update",
    response_model=project.update_preferences_service.UpdateUserPreferencesResponse,
)
async def api_put_update_preferences(
    preference_type: str, value: str
) -> project.update_preferences_service.UpdateUserPreferencesResponse | Response:
    """
    Updates the preferences for the logged-in user.
    """
    try:
        res = await project.update_preferences_service.update_preferences(
            preference_type, value
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refreshes the JWT authentication token using a refresh token.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
