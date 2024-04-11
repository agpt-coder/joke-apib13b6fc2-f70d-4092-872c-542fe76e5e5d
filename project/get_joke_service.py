import random
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class JokeResponse(BaseModel):
    """
    Provides the joke either based on the user's preference or a random selection if no preference is provided. Includes necessary fields for a dad joke.
    """

    setup: str
    punchline: str


async def get_joke(preference: Optional[str] = None) -> JokeResponse:
    """
    Serves a dad joke either randomly or based on the user's preferences.

    Args:
        preference (Optional[str]): An optional user preference to tailor the joke content. Could include categories like 'science', 'history', 'sports', etc. Is ignored if not provided, in which case a random joke is served.

    Returns:
        JokeResponse: Provides the joke either based on the user's preference or a random selection if no preference is provided. Includes necessary fields for a dad joke.
    """
    if preference:
        jokes = await prisma.models.Joke.prisma().find_many(
            where={"setup": {"contains": preference}}, take=10
        )
    else:
        jokes = await prisma.models.Joke.prisma().find_many(take=10)
    if not jokes:
        return JokeResponse(
            setup="Why don't eggs tell jokes?",
            punchline="Because they'd crack each other up.",
        )
    selected_joke = random.choice(jokes)
    return JokeResponse(setup=selected_joke.setup, punchline=selected_joke.punchline)
