"""
helper.py

contains helper functions
"""

import aiohttp

async def get_current_ip() -> str:
    """
    return the current ip address
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api6.ipify.org') as response:
                return await response.text()
    except aiohttp.client_exceptions.ClientConnectorError:
        pass
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api4.ipify.org') as response:
                return await response.text()
    except aiohttp.client_exceptions.ClientConnectorError:
        return "error"
