import os
from openai import OpenAI

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt


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
    owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

    context = {}
    context['owner_chats'] = owner_chats

    return render(request, os.path.join('chat', 'chat.html'), context)

# @login_required
# def chat_view(request):
#     if request.method == 'GET':
#         chat = Chat.objects.create(
#             owner=request.user,
#             title="New Chat",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#             ]
#         )

#         owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

#         request.session['chat_id'] = chat.id

#         context = {}
#         context['chat'] = chat
#         context['owner_chats'] = owner_chats

#         return render(request, os.path.join('chat', 'chat-view.html'), context)
    
#     elif request.method == 'POST':
#         chat_id = request.session.get('chat_id')
#         chat = Chat.objects.get(id=chat_id)

#         user_message = request.POST.get('message', '')

#         new_messages = chat.messages
#         new_messages.append({"role": "user", "content": user_message})

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=new_messages,
#             max_tokens=500
#         )
#         ai_message = response.choices[0].message.content
#         new_messages.append({"role": "assistant", "content": ai_message})

#         chat.messages = new_messages
#         chat.save()

#         return JsonResponse({'message': ai_message})


class CreateChat(LoginRequiredMixin, View):
    def get(self, request):
        owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')
        
        form = ChatForm()

        context = {}
        context['owner_chats'] = owner_chats
        context['form'] = form

        return render(request, os.path.join('chat', 'chat-create.html'), context)

    def post(self, request):
        if 'create' in request.POST:
            form = ChatForm(request.POST)
            
            if form.is_valid():
                chat = form.save(commit=False)

                chat.owner = request.user
                chat.messages = [
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant."
                    },
                ]

                chat.save()

                return redirect("chat-view", chat_id=chat.id)


class ChatView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # manually grab chat id from kwargs and process it
        chat = Chat.objects.get(id=self.kwargs['chat_id'])

        return self.request.user == chat.owner

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

        context = {}
        context['chat'] = chat
        context['owner_chats'] = owner_chats

        return render(request, os.path.join('chat', 'chat-view.html'), context)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        user_message = request.POST.get('message', '')

        new_messages = chat.messages
        new_messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=new_messages,
            max_tokens=500
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
