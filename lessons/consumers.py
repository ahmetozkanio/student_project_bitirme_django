import asyncio
from itertools import count
import json
from webbrowser import get
from django.contrib.auth.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Lesson,Message, OnlineUsers

class LessonConsumers(AsyncConsumer):

    async def websocket_connect(self, event):
  
        # url deki ders id  ve giris yapmis kullanici
        lesson_id_url = self.scope['url_route']['kwargs']['lesson_id']
        user = self.scope['user']
        self.user = user
      
        lesson_obj = await self.get_lesson(lesson_id_url) 
        self.lesson_obj = lesson_obj
        online =await self.create_online_user()
        print(online)


        #online users
        self.onlineusers = await self.get_online_users(lesson_obj.id)
       
        # for onusers in self.onlineusers:
        #     print(onusers)
        


        # chat_room
        self.lesson_id = lesson_id_url
        chat_room =  f"lesson_{lesson_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })

        #close websocket 10 saniye sonra kapanir
        # await asyncio.sleep(10)
        # await self.send({
        # "type": "websocket.close",
        # })
        # Consola bir message yolladik  .send ile
        # await self.send({
        #     "type": "websocket.send",
        #     "text":"Selamlar"
        # })

    async def websocket_receive(self, event):
        print("receive-consumers.py ",event)
        #receive-consumers.py  {'type': 'websocket.receive', 'text': '{"message":"asdas"}'}
     
        # online users
        # self.onlineusers = await self.get_online_users()
        count = await self.count_online_users()
        print(count)
        # await self.channel_layer.group_send(
        #        self.chat_room,
        #        {
        #            "type": "online_users",
        #            "command":'onlineusers',
        #            "count": count,
        #        }
        #    )
      
       
       
        front_text =event.get('text',None)
        if front_text is not None:
           loaded_dict_data = json.loads(front_text)
           msg = loaded_dict_data.get('message')
          
           user = self.scope['user']
           username = 'default_username'
           if user.is_authenticated:
               username = user.username
           myResponse = {
               'message':msg,#brodcast edilen mesaj
               'username':username
           }
           await self.create_chat_message(msg,self.lesson_obj,self.user)
        
           # brodcast message , yayin yapar mesaji
           await self.channel_layer.group_send(
               self.chat_room,
               {
                   "type": "chat_message",
                   "text":json.dumps(myResponse),
                   'command':"msg"
                   
               }
           )

    async def chat_message(self,event):
        print('message',event)
        # mesaj verisi
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })
    @database_sync_to_async
    def get_lesson(self,lesson_id):
        return Lesson.objects.get(id = lesson_id)
    @database_sync_to_async
    def create_chat_message(self,msg,lesson,user):
        return Message.objects.create(text = msg,lesson = lesson, user = user)

    async def online_users(self,event):
        print('online_users -- consumers',event)
        await self.send({
            "type":"websocket.send",
            "text":event['count']
        })
    
    @database_sync_to_async
    def get_online_users(self,id):
        return OnlineUsers.objects.all().filter(lesson__id=id)
    @database_sync_to_async
    def count_online_users(self):
        return OnlineUsers.objects.count()
    @database_sync_to_async
    def create_online_user(self):
        return OnlineUsers.objects.create(user=self.user,lesson =self.lesson_obj)
    @database_sync_to_async
    def delete_online_user(self):
        return OnlineUsers.objects.filter(user=self.user,lesson =self.lesson_obj).delete()
    
    async def websocket_disconnect(self,event):
        print("disconnected - consumers.py" ,event)
        await self.delete_online_user()
        
        # await self.channel_layer.group_discard(
        #     self.chat_room,
        #     self.channel_name
        # )