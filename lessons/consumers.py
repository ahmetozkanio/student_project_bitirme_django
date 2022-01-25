import asyncio
import json
from marshal import dumps
from webbrowser import get
from django.contrib.auth.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core import serializers
from .models import Lesson,Message, OnlineUsers
from asgiref.sync import sync_to_async
class LessonConsumers(AsyncConsumer):

    async def websocket_connect(self, event):
  
        # url deki ders id  ve giris yapmis kullanici
        lesson_id_url = self.scope['url_route']['kwargs']['lesson_id']
        user = self.scope['user']
        self.user = user
      
        lesson_obj = await self.get_lesson(lesson_id_url) 
        self.lesson_obj = lesson_obj
        
      


       
        # for onusers in self.onlineusers:
     
        


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

        front_send_text =event.get('text',None)
        loaded_dict_data = json.loads(front_send_text)
        
        
        
        # online users
        if(loaded_dict_data.get('command') == "connected"):
            await self.create_online_user()
            count = await self.count_online_users()
             #online users
            onlineusers = await self.get_online_users()
            print(onlineusers)
            myResponse = {
                    'count': count,
                    'command':'onlineusers',
                    'onlineusers':onlineusers
                
            }
            await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "online_users",
                        "text":json.dumps(myResponse),

                    }
            )  
        # if loaded_dict_data.get('command')=="closed":
        #     await self.delete_online_user()
        #     count = await self.count_online_users()
        #     myResponse = {
        #             'count': count,
        #             'command':'onlineusers',
                
        #     }
        #     await self.channel_layer.group_send(
        #             self.chat_room,
        #             {
        #                 "type": "online_users",
        #                 "text":json.dumps(myResponse),

        #             }
        #     )  
        if(loaded_dict_data.get('command') == "msg"):
            msg = loaded_dict_data.get('message')
            print(loaded_dict_data)
            user = self.scope['user']
            username = 'default_username'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message':msg,#brodcast edilen mesaj
                'username':username,
                'command':'msg'
            }
            await self.create_chat_message(msg,self.lesson_obj,self.user)
            
            # brodcast message , yayin yapar mesaji
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text":json.dumps(myResponse),

                }
            )
        
      

    async def chat_message(self,event):
        print('messagess chat_message',event)
        # mesaj verisi
        await self.send({
            "type":"websocket.send",
            "text":event['text'],
         
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
            "text":event['text'], 
        })

    @database_sync_to_async
    def get_online_users(self):
        self.online_user_list = []
        users= OnlineUsers.objects.all().filter(lesson =self.lesson_obj)
        for user in users:
            self.online_user_list.append(user.user.username)
        return self.online_user_list





    @database_sync_to_async
    def count_online_users(self):
        return OnlineUsers.objects.all().filter(lesson =self.lesson_obj).count()
    @database_sync_to_async
    def create_online_user(self):
        return OnlineUsers.objects.create(user=self.user,lesson =self.lesson_obj)
    @database_sync_to_async
    def delete_online_user(self):
        return OnlineUsers.objects.filter(user=self.user,lesson =self.lesson_obj).delete()
    
    async def websocket_disconnect(self,event):
        print("disconnected - consumers.py" ,event)
        await self.delete_online_user()
        count = await self.count_online_users()
        onlineusers = await self.get_online_users()
        myResponse = {
                    'count': count,
                    'command':'onlineusers',
                    'onlineusers':onlineusers
                
            }
        await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "online_users",
                        "text":json.dumps(myResponse),

                    }
            )  
        # await self.channel_layer.group_discard(
        #     self.chat_room,
        #     self.channel_name
        # )