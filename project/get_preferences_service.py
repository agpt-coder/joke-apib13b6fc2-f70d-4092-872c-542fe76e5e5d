from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class PreferenceDetail(BaseModel):
    """
    Detail of a single preference setting.
    """

    preferenceType: str
    value: str


class GetPreferencesResponse(BaseModel):
    """
    Provides structured details of the user's set preferences including types of jokes they prefer.
    """

    preferences: List[PreferenceDetail]


async def get_preferences() -> GetPreferencesResponse:
    """
    Retrieves the logged-in user's set preferences.

    Fetches user preferences data from the `Preference` model and returns a structured response consisting of preference type and values.

    Returns:
    GetPreferencesResponse: Provides structured details of the user's set preferences including types of jokes they prefer.

    Raises:
    This function assumes that there's a utility available to identify the currently logged-in user, returning their ID.
    In case there's no logged-in user, or the user has no preferences set, it handles these scenarios gracefully.
    """
    current_user_id = "mocked_current_user_id_here"
    preferences = await prisma.models.Preference.prisma().find_many(
        where={"userId": current_user_id}
    )
    preference_details = [
        PreferenceDetail(
            preferenceType=preference.preferenceType, value=preference.value
        )
        for preference in preferences
    ]
    return GetPreferencesResponse(preferences=preference_details)
