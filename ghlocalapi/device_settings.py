"""
Controll device settings on the unit.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

from .const import API, HEADERS

_LOGGER = logging.getLogger(__name__)


class DeviceSettings(object):
    """A class for device dettings."""

    def __init__(self, loop, session, ipaddress):
        """Initialize the class."""
        self._loop = loop
        self._ipaddress = ipaddress
        self._session = session

    async def reboot(self):
        """Reboot the device."""
        endpoint = '/setup/reboot'
        url = API.format(ip=self._ipaddress, endpoint=endpoint)
        data = {'params': 'now'}
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                await self._session.post(url, body=data, headers=HEADERS)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to GHLocalApi, %s', error)
