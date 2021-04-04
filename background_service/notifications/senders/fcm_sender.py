from channels.db import database_sync_to_async
from account.models import User

class FCMSender:

    @database_sync_to_async
    def send_message(self, msg, user_id):
        user = User.objects.get(id=user_id)
        device = user.get_fcm_device()
        if device:
            device.send_message(msg)

    async def run(self):
        return None
