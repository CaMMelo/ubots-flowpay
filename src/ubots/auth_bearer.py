from uuid import UUID

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer


class BearerToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(BearerToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(BearerToken, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        return credentials.credentials
