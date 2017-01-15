from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,'index.html')

def login_action(request):
    if request.method == "POST":
       username = request.POST.get('username','')
       password = request.POST.get('password','')
       if username == 'gab' and password == 'gab1234':
          return render(request,'event.html')
       else:
          return render(request,'index.html',{'error':'username or password error!'})
