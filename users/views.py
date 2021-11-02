from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
#
from store import views as store_views
#
import json
import paho.mqtt.client as mqtt
from django.shortcuts import render
from django.http import JsonResponse
import datetime


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#    return render(request, 'profile.html')



def backCar(request):

    """
    train_cmd = {
        "Track": 'A1',
        "Position": '00'
    }
    """
    # 電車返回廚房 payload
    train_cmd = {
		"traffic": {"travel": "00"}
	}

    payload = json.dumps(train_cmd) # encode dict oject to JSON

    def connect_msg():
        print('Connect to Broker')


    def publish_msg():
        print('Message Published')

    client = mqtt.Client(client_id='publish-ipadxx') # publisher ipadxx
    client.on_connect = connect_msg()
    client.on_publish = publish_msg()
    client.username_pw_set(username='pub_client', password='password')
    client.connect('127.0.0.1', 1883, 60)
	# client.connect('192.168.50.172', 1883)
	
	# publish to mqtt
    # 電車 A1 返回廚房
    ret = client.publish('tram/v1/cherpa/A1/tell', payload) # payload = {"traffic":{"travel":"00"}} 

    client.loop()
    if ret[0] == 0:
        pass
    else:
        print(f"Failed to send message, return code:", ret[0])
    client.disconnect()

    messages.success(request, f'CyberTrain 已安全返航，敬祝用餐愉快！')
    return redirect('store')
