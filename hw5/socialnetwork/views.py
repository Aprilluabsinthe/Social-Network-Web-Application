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
from socialnetwork.models import Post, Comment, Profile


# ENTRY_LIST = MyMemoryList()


@login_required
def home_action(request):
    try:
        postitems = Post.objects.all()
        comments = Comment.objects.all()
        return render(request, 'socialnetwork/globalstream.html',
                  {'posts': postitems,
                   'comments': comments})
    except:
        return render(request, 'socialnetwork/globalstream.html',{})


@login_required
def followerstream_action(request):
    return render(request, 'socialnetwork/followerstream.html')


@login_required
def globalstream_action(request):
    if request.method == 'GET':
        return render(request, 'socialnetwork/globalstream.html', {})

    return render(request, 'socialnetwork/globalstream.html', {})


@login_required
def makepost(request):
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {}
    if 'post' not in request.POST or not request.POST['post']:
        context['error'] = 'You must enter an content of a post'
        return render(request, 'socialnetwork/globalstream.html', context)
    context = {'posts': Post.objects.all()}
    new_post = Post(user=request.user,
                    content=request.POST['post'])
    new_post.save()
    return redirect('home')


@login_required
def makecomment(request):
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {'posts': Post.objects.all()}
    if 'comment' not in request.POST or not request.POST['comment']:
        context['error'] = 'You must enter an content of a comment'
        return render(request, 'socialnetwork/globalstream.html', context)

    context = {'comments': Comment.objects.all()}
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


# @login_required
# def edit_action(request, id):
#     if request.method == 'GET':
#         form = ProfileForm(entry)
#         context = {'entry': entry, 'form': form}
#         return render(request, 'socialnetwork/edit.html', context)
#     #
#     edit_form = ProfileForm(request.POST)
#     if not edit_form.is_valid():
#         context = {'form': edit_form, 'entry': entry}
#         return render(request, 'socialnetwork/edit.html', context)
#
#     for field in ['last_name', 'first_name', 'birthday', 'children',
#                   'address', 'city', 'state', 'zip_code', 'country',
#                   'email', 'phone_number']:
#         entry[field] = edit_form.cleaned_data[field]


#     entry['updated_by'] = request.user
#     entry['update_time'] = timezone.now()
#
#     ENTRY_LIST.update(entry)
#
#     message = 'Entry Updated'
#     context = {'message': message, 'entry': entry, 'form': edit_form}
#     return render(request, 'socialnetwork/edit.html', context)
#
#     context = {'posts': Post.objects.all()}
#
#     if request.method != 'POST':
#         context['error'] = 'Editions must be done using the POST method'
#         return render(request, 'socialnetwork/globalstream.html', context)
#
#     # Deletes the item if present in the database.
#     try:
#         post_to_edit = Post.objects.get(id=post_id)
#         if request.user.username != post_to_edit.user.username:
#             context['error'] = 'You can only edit Posts you have created.'
#             return redirect('home')
#
#         post_to_edit[]
#         return redirect('home')
#     except ObjectDoesNotExist:
#         context['error'] = 'The item did not exist in the To Do List.'
#         return redirect('home')
#
#
def myprofile_action(request):
    return render(request, 'socialnetwork/profile.html')


def profile_others(request):
    return render(request, 'socialnetwork/profile_others.html')


def profile_home(request):
    context = {}
    context['profile'] = Profile.objects.all()
    context['profileform'] = ProfileForm()
    return render(request, 'socialnetwork/profile.html', context)


def add_profile(request):
    context = {}
    if request.method == 'GET':
        f = ProfileForm()
        context = {'profileform': f}
        return render(request, 'socialnetwork/profile.html', context)

    new_profile = Profile(user=request.user)
    profileform = ProfileForm(request.POST, request.FILES, instance=new_profile)

    if not profileform.is_valid():
        context['profileform'] = profileform
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        # pic = profileform.cleaned_data['picture']
        profileform.save()
        context['message'] = 'Profile #{0} saved.'.format(new_profile.id)
        context['profileform'] = ProfileForm()

    context['profile'] = Profile.objects.get(user=request.user)
    # return render(request, 'socialnetwork/profile.html', context)
    return render(request, 'socialnetwork/profileshow.html', context)


@login_required
def get_profile(request, userid):
    user = User.objects.get(id=userid)
    profileitem = Profile()
    try:
        profileitem = get_object_or_404(Profile, user_id=userid)
        context = {}
        context['profile'] = profileitem
        context['profileform'] = ProfileForm()
        return render(request, 'socialnetwork/profileshow.html', context)
    except Http404:
        return redirect('add-profile')


@login_required
def get_photo(request, id):
    profileitem = get_object_or_404(Profile, user=id)
    print('profileitem #{} fetched from db : {}'.format(id, profileitem.picture))
    if not profileitem.picture:
        raise Http404
    return HttpResponse(profileitem.picture)


def delete_profile(request):
    return render(request, 'socialnetwork/profile_others.html')


def edit_profile(request):
    return render(request, 'socialnetwork/profile_others.html')


# @login_required
# def create_action(request):
#     if request.method == 'GET':
#         context = {'form': ProfileForm()}
#         return render(request, 'socialnetwork/create.html', context)
#
#     form = ProfileForm(request.POST)
#     if not form.is_valid():
#         context = {'form': form}
#         return render(request, 'socialnetwork/create.html', context)
#
#     my_entry = {}
#     for field in ['last_name', 'first_name', 'birthday', 'children',
#                   'address', 'city', 'state', 'zip_code', 'country',
#                   'email', 'phone_number']:
#         my_entry[field] = form.cleaned_data[field]
#
#     my_entry['created_by'] = request.user
#     my_entry['creation_time'] = timezone.now()
#     my_entry['updated_by'] = request.user
#     my_entry['update_time'] = timezone.now()
#
#     ENTRY_LIST.create(my_entry)
#
#     message = 'Entry created'
#     new_form = ProfileForm(my_entry)
#     context = {'message': message, 'entry': my_entry, 'form': new_form}
#     return render(request, 'socialnetwork/edit.html', context)
#


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
