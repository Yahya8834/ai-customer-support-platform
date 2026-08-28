from channels.layers import get_channel_layer
from django.test import TransactionTestCase



class ChannelLayerTests(TransactionTestCase):

    async def test_channel_layer_can_send_and_receive(self):
        channel_layer = get_channel_layer()

        channel_name = await channel_layer.new_channel()

        await channel_layer.send(
            channel_name,
            {
                "type": "test.message",
                "message": "hello redis",
            },
        )

        message = await channel_layer.receive(channel_name)

        self.assertEqual(
            message["type"],
            "test.message",
        )
        self.assertEqual(
            message["message"],
            "hello redis",
        )