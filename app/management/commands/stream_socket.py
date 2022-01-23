import time

import psutil
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management import BaseCommand

from system.settings import STREAM_SOCKET_GROUP_NAME


class Command(BaseCommand):
    help = 'Command to start stream socket data if any socket open'

    def handle(self, *args, **options):
        group_name = STREAM_SOCKET_GROUP_NAME
        channel_layer = get_channel_layer()

        # psutil library useful to retrieve system uses the percent of CPU and RAM
        # cpu_percent = psutil.cpu_percent()
        # ram_percent = psutil.virtual_memory().percent

        # Testing simulation of a cronjob calling the function multiple times
        for x in range(100):
            # simulate changes in the values of cpu and ram
            cpu_percent = random.randint(1, 100)
            ram_percent = random.randint(1, 100)

            # convert group_send function from async to sync method
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'system_load',
                    'data': {
                        'cpu_percent': cpu_percent,
                        'ram_percent': ram_percent
                    }
                }
            )
            time.sleep(5)
