""" http transport implementation using httpx """

import httpx

from transport.http import Request, Response

async def send(request: Request) -> Response:
    raise NotImplementedError()
    # need to convert to httpx and back
    async with httpx.AsyncClient() as client:
        response = await client.send(request)
        return response
