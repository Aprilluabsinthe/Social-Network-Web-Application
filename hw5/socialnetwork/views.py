from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import ProfileForm, LoginForm, RegisterForm, PostForm

# from socialnetwork.MyMemoryList import MyMemoryList
from socialnetwork.models import Post, Comment, Profile, Friendship


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
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {}
    if 'post' not in request.POST or not request.POST['post']:
        context['error'] = 'You must enter an content of a post'
        return render(request, 'socialnetwork/globalstream.html', context)

    context = {'posts': Post.objects.all().order_by('-time')}
    print(context)
    new_post = Post(user=request.user,
                    content=request.POST['post'])
    new_post.save()
    return redirect('home')


@login_required
def makecomment(request):
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {'posts': Post.objects.all().order_by('-time')}
    if 'comment' not in request.POST or not request.POST['comment']:
        context['error'] = 'You must enter an content of a comment'
        return render(request, 'socialnetwork/globalstream.html', context)

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
    friendsets = Friendship.objects.filter(user_id=request.user.id)
    if friendsets:
        context['friends'] = []
        for friend in friendsets:
            context['friends'].append(friend.friend)
            print(context['friends'])

    if request.method == 'GET':
        f = ProfileForm()
        context['profileform'] = f
        return render(request, 'socialnetwork/profile.html', context)

    new_profile = Profile(user=request.user)
    profileform = ProfileForm(request.POST, request.FILES, instance=new_profile)

    if not profileform.is_valid():
        context['profileform'] = profileform
    else:
        profileform.save()
        context['message'] = 'Profile #{0} saved.'.format(new_profile.user)
        context['profileform'] = ProfileForm()
    context['profile'] = Profile.objects.get(user=request.user)
    return redirect('profile', userid=request.user.id)


@login_required
def get_profile(request, userid):
    user = User.objects.get(id=userid)
    profileitem = Profile()
    try:
        profileitem = get_object_or_404(Profile, user_id=userid)
        context = {}
        context['profile'] = profileitem
        context['profileform'] = ProfileForm(
            initial={'bio': profileitem.bio, 'picture': profileitem.picture})

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
        return render(request, 'socialnetwork/profileshow.html', context)

    except Http404:
        print("some exception happends, redirect to my profile")
        return redirect('add-profile')


@login_required
def get_photo(request, id):
    profileitem = get_object_or_404(Profile, id=id)
    print('profileitem picture#{} fetched from db : {}'.format(id, profileitem.picture))
    if not profileitem.picture:
        raise Http404
    return HttpResponse(profileitem.picture, content_type='image/jpeg/jpg/png')


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
