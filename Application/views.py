from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import HttpResponse
import datetime
from Application.models import *
from channels.layers import channel_layers,get_channel_layer

def indexpage(request):
    c=notifyform.objects.count()
    data=notifyform.objects.all().order_by("-date")[:5]
    return render(request,'index.html',{'data':data, 'c':c,'room_name':'broadcast'})

def submit(request):
    if request.method == 'POST':
        image = request.POST['imageupload']
    today=datetime.datetime.now()
    # Date=today.strftime("%A")
    obj=notifyform(images=image,date=today)
    obj.save()
    return HttpResponseRedirect("/")

def old(request):
    return render(request,'old.html')
