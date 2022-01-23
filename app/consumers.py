"""
    AsyncWebsocketConsumer and async/await, we use class and Asynchronous I/O,
    because Django Channel Library has functions send(), group_send(), group_add()
    that are async functions, so we are using these functions in method of our class,
    so we Inherit AsyncWebsocketConsumer class and async/await I/O.

    1 Connect method call from a client and when client first time makes the connection with Websocket.
    2. Disconnect method will call client close the tab and maybe client disconnect website using some event from browser.
    3. Receive method call when client sends some message to the server through WebSocket.
    4. System Load method is an event method that calls when group_send method of channel layer uses type as "system_load" method name.
    5. System load method sends data to client and the client uses that data to represent on browser according to requirements.
    6. According to the code, when the client send a message to the server using WebSocket then Websocket return system default uses of RAM and CPU as 0
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer

from system.settings import STREAM_SOCKET_GROUP_NAME


class SystemConsumer(AsyncWebsocketConsumer):
    group_name = STREAM_SOCKET_GROUP_NAME

    async def connect(self):
        # joining group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # receive data from websocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'system_load',
                'data': {
                    'cpu_percent': 0,
                    'ram_percent': 0
                }
            }
        )

    async def system_load(self, event):
        # receive data from group
        await self.send(
            text_data=json.dumps(event['data'])
        )