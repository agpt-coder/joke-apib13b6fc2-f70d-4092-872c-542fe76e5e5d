import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirmation of feedback submission by the user.
    """

    success: bool
    message: str


async def submit_feedback(
    userId: str, feedbackContent: str, feedbackType: str
) -> SubmitFeedbackResponse:
    """
    Allows users to submit feedback about the app or the jokes.

    Args:
        userId (str): The unique identifier of the user submitting feedback.
        feedbackContent (str): The content of the feedback submitted by the user.
        feedbackType (str): The type of feedback being submitted (e.g., 'app', 'joke').

    Returns:
        SubmitFeedbackResponse: Confirmation of feedback submission by the user.

    This function leverages the Prisma ORM to interact with the database, specifically,
    to add a new feedback entry linked to the user. It checks for the existence of the user
    before attempting to insert the feedback. A successful operation returns a response
    indicating success, otherwise, it signals a failure.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": userId})
        if not user:
            return SubmitFeedbackResponse(success=False, message="User not found.")
        await prisma.models.Feedback.prisma().create(
            data={
                "userId": userId,
                "content": feedbackContent,
                "feedbackType": feedbackType,
            }
        )
        return SubmitFeedbackResponse(
            success=True, message="Feedback submitted successfully."
        )
    except Exception as e:
        print(f"Exception while submitting feedback: {e}")
        return SubmitFeedbackResponse(
            success=False, message="An error occurred while submitting feedback."
        )
