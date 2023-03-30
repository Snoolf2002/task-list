from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate
from base64 import b64decode
import json

from .models import Task
from django.contrib.auth.models import User


def isAuth(auth):
    if auth is None:
        return False
    
    token = auth.split(' ')[1]
    auth=b64decode(token).decode() # Decode token
    username, password = auth.split(':') # Split token

    user = authenticate(username=username, password=password)

    if user is not None:
        return True
    
    return False

# Create task and get all tasks
def tasks(request: HttpRequest) -> JsonResponse:
    auth = request.headers.get('Authorization')

    if isAuth(auth):
        token = auth.split(' ')[1]
        auth=b64decode(token).decode() # Decode token
        username, password = auth.split(':') # Split token
        user = authenticate(username=username, password=password)

        if request.method == 'POST':
            decoded = request.body.decode()
            data = json.loads(decoded)

            task = Task()
            task.title = data.get('title')
            task.descreption = data.get('descreption')
            task.status = data.get('status', False)
            task.user = user
            task.save()

            return JsonResponse({"status": 200})
        
        if request.method == 'GET':
            tasks = Task.objects.filter(user=user)

            data = {
                'tasks': []
            }
            for i in tasks:
                data['tasks'].append(
                    {
                        "id": i.id,
                        'title': i.title,
                        'descreption': i.descreption,
                        'status': i.status
                    }
                )
            return JsonResponse(data)
        
    return JsonResponse({'Status': 'Hey, you are not authenticated!!'})


# get task and update task with id
def get_task(request:HttpRequest, pk):
    auth = request.headers.get('Authorization')
    if isAuth(auth):
        token = auth.split(' ')[1]
        auth=b64decode(token).decode() # Decode token
        username, password = auth.split(':') # Split token
        user = authenticate(username=username, password=password)
        try:
            task = Task.objects.get(id=pk, user=user)
        except:
            return JsonResponse({'status': "This task didn't find"})
        
        if request.method == 'GET':
            data = {
                "id": task.id,
                "title": task.title,
                "descreption": task.descreption,
                "status": task.status
            }
            return JsonResponse(data)
        
        if request.method == 'POST':
            decoded = request.body.decode()
            data = json.loads(decoded)

            if data.get('title') is not None:
                task.title = data.get('title')

            if data.get('descreption') is not None:
                task.descreption = data.get('descreption')

            if data.get('status') is not None:
                task.status = data.get('status')
            task.save()

            data = {
                "id": task.id,
                "title": task.title,
                "descreption": task.descreption,
                "status": task.status
            }
            return JsonResponse(data)
