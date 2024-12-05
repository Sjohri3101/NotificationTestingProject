from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':"connected to django channel"}))

    def receive(self,text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status':"we got you"}))
        
    def disconnect(self, *args,**kwargs):
        print("disconnected")
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
        
    def send_notification(self,event):
        print("send notification")
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({"payload": data}))
        