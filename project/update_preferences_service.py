import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserPreferencesResponse(BaseModel):
    """
    Confirmation response indicating the success of preference update operation.
    """

    success: bool
    message: str


async def update_preferences(
    preference_type: str, value: str
) -> UpdateUserPreferencesResponse:
    """
    Updates the preferences for the logged-in user.

    This function assumes that the user is already authenticated and their user ID is somehow retrievable.
    For this implementation, let's assume there is a context manager or a mechanism (not shown here) to get the logged-in user's ID.

    It queries the Preference model for the user's existing preferences of the provided type,
    updates the value if it exists, or creates a new Preference record if it doesn't.

    Args:
        preference_type (str): The type of preference the user wishes to update.
        value (str): The new value for the specified preference type.

    Returns:
        UpdateUserPreferencesResponse: Confirmation response indicating the success of preference update operation.
    """
    user_id = "current_user_id"
    preference = await prisma.models.Preference.prisma().find_first(
        where={"userId": user_id, "preferenceType": preference_type}
    )
    if preference:
        await prisma.models.Preference.prisma().update(
            where={"id": preference.id}, data={"value": value}
        )
        message = "Preference updated successfully."
    else:
        await prisma.models.Preference.prisma().create(
            data={"userId": user_id, "preferenceType": preference_type, "value": value}
        )
        message = "Preference created successfully."
    return UpdateUserPreferencesResponse(success=True, message=message)
