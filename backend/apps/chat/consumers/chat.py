from channels.generic.websocket import WebsocketConsumer



class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        self.send(
            text_data="connected",
        )

    def disconnect(self, close_code):
        pass