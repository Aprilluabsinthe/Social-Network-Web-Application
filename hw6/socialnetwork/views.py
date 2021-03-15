import json
from datetime import datetime
from json import JSONEncoder

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from socialnetwork.forms import ProfileForm, LoginForm, RegisterForm, PostForm

# from socialnetwork.MyMemoryList import MyMemoryList
from socialnetwork.models import Post, Comment, Profile, Friendship, AjaxItem
import json
import  datetime


# ENTRY_LIST = MyMemoryList()


@login_required
def home_action(request):
    try:
        postitems = Post.objects.all().order_by('-time')
        comments = Comment.objects.all().order_by('-time')
        return render(request, 'socialnetwork/globalstream.html',
                      {'posts': postitems,
                       'comments': comments})
    except:
        return render(request, 'socialnetwork/globalstream.html', {})


@login_required
def followerstream_action(request):
    friends = Friendship.objects.filter(user_id=request.user.id)
    print(friends)
    seeonly = []
    if friends.exists():
        for friend in friends:
            seeonly.append(friend.friend)
    print(seeonly)
    postitems = Post.objects.filter(user__in=seeonly).order_by('-time')
    comments = Comment.objects.all().order_by('-time')
    return render(request, 'socialnetwork/followerstream.html',
                  {'posts': postitems,
                   'comments': comments})


@login_required
def globalstream_action(request):
    return redirect('home')


@login_required
def makepost(request):
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    if not 'post' in request.POST or not request.POST['post']:
        return _my_json_error_response("You must enter an post to add.")

    context = {}

    print("enter making posts")
    if Post.objects.all():
        context = {'posts': Post.objects.all().order_by('-time')}
        print(context)

    new_post = Post(user=request.user,
                    content=request.POST['post'])
    new_post.save()
    # return redirect('home')
    return get_global_django_serializer(request)


@login_required
def makecomment(request):
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {'posts': Post.objects.all().order_by('-time')}

    if 'comment' not in request.POST or not request.POST['comment']:
        context['error'] = 'You must enter an content of a comment'
        return render(request, 'socialnetwork/globalstream.html', context)

    # thiscomments = Comment.objects.filter(parentpost = )
    context = {'comments': Comment.objects.all().order_by('-time')}
    new_comment = Comment(user=request.user,
                          content=request.POST['comment'],
                          )
    new_comment.save()
    return redirect('home')


@login_required
def delete_action_post(request, post_id):
    context = {'posts': Post.objects.all()}

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, 'socialnetwork/globalstream.html', context)

    # Deletes the item if present in the database.
    try:
        post_to_delete = Post.objects.get(id=post_id)
        if request.user.username != post_to_delete.user.username:
            context['error'] = 'You can only delete Posts you have created.'
            return redirect('home')

        post_to_delete.delete()
        return redirect('home')
    except ObjectDoesNotExist:
        context['error'] = 'The item did not exist in the To Do List.'
        return redirect('home')


@login_required
def delete_action_comment(request, comment_id):
    context = {'comments': Comment.objects.all()}

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, 'socialnetwork/globalstream.html', context)

    # Deletes the item if present in the database.
    try:
        comment_to_delete = Comment.objects.get(id=comment_id)
        if request.user.username != comment_to_delete.user.username:
            context['error'] = 'You can only delete comments you have created.'
            return redirect('home')

        comment_to_delete.delete()
        return redirect('home')
    except ObjectDoesNotExist:
        context['error'] = 'The item did not exist in the To Do List.'
        return redirect('home')


def profile_others(request):
    return render(request, 'socialnetwork/profile_others.html')


def profile_home(request):
    context = {}
    context['profile'] = Profile.objects.all()
    context['profileform'] = ProfileForm()
    return render(request, 'socialnetwork/profile.html', context)


def add_profile(request):
    context = {}
    print(request.user)
    new_profile = Profile(user=request.user)
    print(new_profile)
    profileform = ProfileForm(request.POST, request.FILES, instance=new_profile)

    friendsets = Friendship.objects.filter(user_id=request.user.id)
    if friendsets:
        context['friends'] = []
        for friend in friendsets:
            context['friends'].append(friend.friend)
            print(context['friends'])

    if request.method == 'GET':
        f = ProfileForm()
        context['profile'] = new_profile
        context['profileform'] = ProfileForm()
        print("method is GET")
        print(context)
        return render(request, 'socialnetwork/profile.html', context)

    if not profileform.is_valid():
        context['profileform'] = profileform

    else:
        profileform.save()
        context['message'] = 'Profile #{0} saved.'.format(new_profile.user)
        context['profileform'] = ProfileForm()
    context['profile'] = Profile.objects.get(user=request.user)
    # return render(request, 'socialnetwork/profileshow.html', context)
    return redirect('profile', userid=request.user.id)


@login_required
def get_profile(request, userid):
    context = {}

    if userid != request.user.id:
        friendship = Friendship.objects.filter(user_id=request.user.id, friend_id=userid)
        if friendship.exists():
            context['follow_action'] = 'Unfollow'
        else:
            context['follow_action'] = 'Follow'
    else:
        friendsets = Friendship.objects.filter(user_id=request.user.id)
        if friendsets:
            context['friends'] = []
            for friend in friendsets:
                context['friends'].append(friend.friend)
    print(context)

    try:
        profileitem = get_object_or_404(Profile, user_id=userid)
        context['profile'] = profileitem
        context['profileform'] = ProfileForm(
            initial={'bio': profileitem.bio, 'picture': profileitem.picture})
        print("got profile file")
        return render(request, 'socialnetwork/profileshow.html', context)
    except Http404:
        if userid == request.user.id:
            print("redirect to add my profile")
            return redirect('add-profile')
        else:
            profileitem = Profile(user_id=userid)
            context['profile'] = profileitem
            context['profileform'] = ProfileForm()
        return render(request, 'socialnetwork/profile.html', context)

    # except Http404:
    #     if userid == request.user.id:
    #         print("redirect to add my profile")
    #         return redirect('add-profile')
    #     else:
    #         profileitem = Profile(user_id=userid)
    #         context['profileform'] = ProfileForm()
    #         return render(request, 'socialnetwork/profile.html', {})


@login_required
def get_photo(request, id):
    try:
        profileitem = get_object_or_404(Profile, id=id)
        print('profileitem picture#{} fetched from db : {}'.format(id, profileitem.picture))
        return HttpResponse(profileitem.picture, content_type='image/jpeg/jpg/png')
    except:
        return HttpResponse('static/media/placeholder.jpg', content_type='image/jpeg/jpg/png')


@login_required
def get_bio(request, id):
    profileitem = get_object_or_404(Profile, id=id)
    print('profileitem biography#{} fetched from db : {}'.format(id, profileitem.bio))
    if not profileitem.bio:
        raise Http404
    return HttpResponse(profileitem.bio)


def delete_profile(request):
    return render(request, 'socialnetwork/profile_others.html')


@login_required
def edit_profile(request, id):
    context = {}
    user = User.objects.get(id=id)
    profileitem = get_object_or_404(Profile, user_id=id)

    if request.user != profileitem.user:
        context = {'message': 'You can only edit items you have created.'}
        return render(request, 'socialnetwork/profileshow.html', context)

    if request.method == 'GET':
        context = {'profile': profileitem,
                   'profileform': ProfileForm(initial={'bio': profileitem.bio, 'picture': profileitem.picture})}
        return render(request, 'socialnetwork/profileshow.html', context)

    profileform = ProfileForm(request.POST, request.FILES)
    print("upload successfully")
    if not profileform.is_valid():
        context = {'profile': profileitem,
                   'profileform': profileform}
        return redirect('profile', userid=id)

    pic = profileform.cleaned_data['picture']
    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))

    profileitem.picture = profileform.cleaned_data['picture']
    profileitem.bio = profileform.cleaned_data['bio']
    profileitem.save()

    context['profile'] = Profile.objects.get(user_id=id)
    # return render(request, 'socialnetwork/profile.html', context)
    return redirect('profile', userid=request.user.id)


@login_required
def changefollow(request, id):
    if request.method == "GET":
        return redirect('profile', userid=id)
    user = User.objects.get(id=request.user.id)
    friend_user = User.objects.get(id=id)
    f = Friendship.objects.filter(user=request.user, friend=friend_user)
    if f.exists():
        f.delete()
        print("delete friendship {} to {}".format(request.user.username, friend_user))
        return redirect('profile', userid=id)
    else:
        friendship = Friendship.objects.create(user=user, friend=friend_user)
        print("add friendship {} to {}".format(request.user.username, friend_user))
        friendship.save()
        return redirect('profile', userid=id)


def get_friend(request, id):
    if request.method == "GET":
        return redirect('profile', userid=id)
    user = User.objects.get(id=request.user.id)
    friend_user = User.objects.get(id=id)
    f = Friendship.objects.filter(user=request.user, friend=friend_user)
    return HttpResponse(f)


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('home'))


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def get_global_json_dumps_serializer(request):
    response_data = []
    for model_item in Post.objects.all():
        my_post = {
            'usr': model_item.user.username,
            'content': model_item.content,
            'time': model_item.time,
        }
        response_data.append(my_post)

    response_json = json.dumps(response_data,cls=DateTimeEncoder)

    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_global_django_serializer(request):
    response_json = serializers.serialize('xml', Post.objects.all())
    return HttpResponse(response_json, content_type='application/xml')

def get_global_xml(request):
    response_json = serializers.serialize('xml', Post.objects.all())
    return HttpResponse(response_json,content_type='application/json')

def get_globalxml_template(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'socialnetwork/posts.xml', context, content_type='application/xml')

def get_follower_xml_template(request):
    friends = Friendship.objects.filter(user_id=request.user.id)
    print(friends)
    seeonly = []
    if friends.exists():
        for friend in friends:
            seeonly.append(friend.friend)
    print(seeonly)
    postitems = Post.objects.filter(user__in=seeonly).order_by('-time')
    comments = Comment.objects.all().order_by('-time')
    context = {'posts': postitems,
                   'comments': comments}
    return render(request, 'socialnetwork/posts.xml', context, content_type='application/xml')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)
