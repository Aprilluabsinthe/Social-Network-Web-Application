import json
import datetime
from json import JSONEncoder

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
from socialnetwork.models import Post, Comment, Profile, Friendship, Commentship
from collections import OrderedDict


# ENTRY_LIST = MyMemoryList()


@login_required
def home_action(request):
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
    # comments = Comment.objects.all().order_by('-time')
    return render(request, 'socialnetwork/followerstream.html', {})


@login_required
def globalstream_action(request):
    return redirect('home')


@login_required
def makepost(request):
    if not request.user:
        return _my_json_error_response("You must be logged in to do this operation", status=403)

    if 'post' not in request.POST or not request.POST['post']:
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    new_post = Post(user=request.user,
                    content=request.POST['post'])
    new_post.save()
    return get_global_json_dumps_serializer(request)


@login_required
def delete_action_post(request, post_id):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=403)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    # Deletes the item if present in the database.
    try:
        post_to_delete = Post.objects.get(id=post_id)
        if request.user.username != post_to_delete.user.username:
            return _my_json_error_response("You cannot delete other user's entries", status=403)

        commentship = Comment.objects.filter(parentpost=post_to_delete)
        print(commentship)
        for comment in commentship:
            print("delete comment")
            comment.delete()
        print("delete commentship")
        commentship.delete
        print("delete post")
        post_to_delete.delete()
        return get_global_json_dumps_serializer(request)
    except ObjectDoesNotExist:
        return _my_json_error_response(f"Post with id={post_id} does not exist.", status=404)


@login_required
def delete_action_comment(request, comment_id):
    print("enter delete_action_comment")
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=403)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    # Deletes the item if present in the database.
    try:
        comment_to_delete = Comment.objects.get(id=comment_id)
        if request.user.username != comment_to_delete.user.username:
            return _my_json_error_response("You cannot delete other user's entries", status=403)

        commentship = Commentship.objects.get(comment=comment_to_delete)
        mainpost = commentship.mainpost
        print(f"mainpostid = {mainpost.id}")
        commentship.delete()
        print("delete post")
        comment_to_delete.delete()
        return get_comment_byid_json_dumps_serializer(request, mainpost.id)
    except ObjectDoesNotExist:
        return _my_json_error_response(f"Comment with id={comment_id} does not exist.", status=404)


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


def addcomment(request, post_id):
    print("enter addcomment")
    if request.method != 'POST':
        print("err1")
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        print("err2")
        return _my_json_error_response("You must enter an comment_text to add.")

    content = request.POST["comment_text"]
    mainpost = Post.objects.get(id=post_id)
    newcomment = Comment.objects.create(
        parentpost=mainpost,
        user=request.user,
        content=content,
    )
    newcomment.save()
    print("save newcomment")
    commentship = Commentship.objects.create(
        mainpost=mainpost,
        comment=newcomment
    )
    commentship.save()
    print("save commentship")
    print(newcomment)
    print(commentship)
    return get_comment_json_dumps_serializer(request)


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


@login_required
def get_profile_byname(request, username):
    context = {}
    profile_user = User.objects.get(username=username)
    # profile_user = Profile.objects.filter(user=username)
    # get_object_or_404(Profile, user=username)
    return redirect('profile', userid=profile_user.id)


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
            'post_id': model_item.id,
            'user': model_item.user.username,
            'first_name': model_item.user.first_name,
            'last_name': model_item.user.last_name,
            'content': model_item.content,
            'time': model_item.time,
        }
        response_data.append(my_post)

    # response_data.sort(key=lambda x: x["time"], reverse=True)
    response_json = json.dumps(response_data, cls=DateTimeEncoder)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_follower_json_dumps_serializer(request):
    friends = Friendship.objects.filter(user_id=request.user.id)
    print(friends)
    seeonly = []
    if friends.exists():
        for friend in friends:
            seeonly.append(friend.friend)
    print(seeonly)
    postitems = Post.objects.filter(user__in=seeonly).order_by('-time')

    response_data = []
    for model_item in postitems:
        follower_post = {
            'post_id': model_item.id,
            'user': model_item.user.username,
            'first_name': model_item.user.first_name,
            'last_name': model_item.user.last_name,
            'content': model_item.content,
            'time': model_item.time,
        }
        response_data.append(follower_post)

    response_data.sort(key=lambda x: x["time"], reverse=False)
    response_json = json.dumps(response_data, cls=DateTimeEncoder)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_comment_json_dumps_serializer(request):
    comments = Commentship.objects.all()
    print(comments)

    response_data = []
    for model_item in comments:
        follower_post = {
            'mainpost': model_item.mainpost,
            'mainpost_id': model_item.mainpost.id,
            'mainuser': model_item.mainpost.user.username,
            'maincontent': model_item.mainpost.content,
            'maintime': model_item.mainpost.time,
            'comment_id': model_item.comment.id,
            'commentuser': model_item.comment.user.username,
            'commentuser_firstname': model_item.comment.user.first_name,
            'commentuser_lastname': model_item.comment.user.last_name,
            'commentcontent': model_item.comment.content,
            'commenttime': model_item.comment.time,
        }
        response_data.append(follower_post)

    # response_data.sort(key=lambda x: x["commenttime"], reverse=True)
    response_json = json.dumps(response_data, cls=DateTimeEncoder)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_comment_byid_json_dumps_serializer(request, post_id):
    commentships = Commentship.objects.filter(mainpost=post_id)
    comments = []
    for commentship in commentships:
        comments.append(commentship.comment)
    print(comments)

    response_data = []
    for model_item in comments:
        follower_post = {
            'parentpost_id': model_item.parentpost.id,
            'parentpostuser': model_item.parentpost.user.username,
            'parentpostcontent': model_item.parentpost.content,
            'parentposttime': model_item.parentpost.time,
            'comment_id': model_item.id,
            'commentuser': model_item.user.username,
            'commentuser_firstname': model_item.user.first_name,
            'commentuser_lastname': model_item.user.last_name,
            'commentcontent': model_item.content,
            'commenttime': model_item.time,
        }
        response_data.append(follower_post)

    # response_data.sort(key=lambda x: x["commenttime"],reverse=True)
    response_json = json.dumps(response_data, cls=DateTimeEncoder)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def sort_by_time(list, keyname):
    # Python dicts do not hold their ordering so we need to make it an
    # ordered dict, after sorting.
    return list.sorted(
        key=lambda x: x[str(keyname)],
        reverse=True
    )
