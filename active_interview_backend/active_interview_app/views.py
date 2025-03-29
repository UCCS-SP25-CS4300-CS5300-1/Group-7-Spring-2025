import os
from openai import OpenAI

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .serializers import *


# Init openai client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# Create your views here.
def index(request):
    return render(request, 'index.html')

def demo(request):
    return render(request, os.path.join('demo', 'demo.html'))

@login_required
def chat(request):
    return render(request, 'chat.html')


@login_required
@csrf_exempt
def test_chat_view(request):
    if request.method == 'GET':
        chat = Chat.objects.create(
            owner=request.user,
            title="new chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
            ]
        )

        request.session['chat_id'] = chat.id

        return render(request, 'chat-test.html')
    
    elif request.method == 'POST':
        chat_id = request.session.get('chat_id')
        chat = Chat.objects.get(id=chat_id)

        user_message = request.POST.get('message', '')

        new_messages = chat.messages
        new_messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=new_messages,
            max_tokens=200
        )
        ai_message = response.choices[0].message.content
        new_messages.append({"role": "assistant", "content": ai_message})

        chat.messages = new_messages
        chat.save()

        return JsonResponse({'message': ai_message})


@login_required
def loggedin(request):
    return render(request, 'loggedinindex.html')


def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='manager_role')
        user.groups.add(group)
        #user = User.objects.create(user=user)
        user.save()
        messages.success(request, 'Account was create for ' + username)
        return redirect('login')
    context={'form':form}
        
    return render(request, 'register.html', context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('logout')
    return render(request, 'logout.html')
