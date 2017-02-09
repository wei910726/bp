from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from poll.models import Event, Guest


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600)
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event.html', {'user': username, 'events': event_list})


@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest.html', {'user': username, 'guests': contacts})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event.html', {'user': username, 'events': event_list})


@login_required
def search_gname(request):
    username = request.session.get('user', '')
    search_gname = request.GET.get('realname', '')
    guest_list = Guest.objects.filter(realname__contains=search_gname)
    return render(request, 'guest.html', {'user': username, 'guests': guest_list})


@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error or event_id error'})

    result = Guest.objects.get(phone=phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return render(request, 'sign_index.html', {'event':event, 'hint': 'sign in success!', 'guest': result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response
