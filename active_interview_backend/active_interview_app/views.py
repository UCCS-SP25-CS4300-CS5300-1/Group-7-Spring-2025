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


# @csrf_exempt
# def test_chat_view(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('message', '')
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": user_message},
#             ],
#             max_tokens=200
#         )
#         ai_message = response.choices[0].message.content
#         return JsonResponse({'message': ai_message})
    
#     return render(request, 'chat-test.html')

@csrf_exempt
def test_chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # ensure you're using a valid model name
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=200
            )
            # Log the raw response for debugging:
            print("OpenAI response:", response)

            # Check if choices exist and have the expected structure
            if (hasattr(response, "choices") and response.choices 
                and hasattr(response.choices[0], "message") and hasattr(response.choices[0].message, "content")):
                ai_message = response.choices[0].message.content
            else:
                raise ValueError("Unexpected response structure: {}".format(response))

            return JsonResponse({'message': ai_message})
        except Exception as e:
            # Log the error details
            import logging
            logging.exception("Error processing OpenAI response:")
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'chat-test.html')



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
