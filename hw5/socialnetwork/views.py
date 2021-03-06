from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import ProfileForm, LoginForm, RegisterForm, PostForm

from socialnetwork.MyMemoryList import MyMemoryList
from socialnetwork.models import Post, Comment

ENTRY_LIST = MyMemoryList()


@login_required
def home_action(request):
    return render(request, 'socialnetwork/globalstream.html',
                  {'posts': Post.objects.all(), 'comments': Comment.objects.all()})


@login_required
def followerstream_action(request):
    return render(request, 'socialnetwork/followerstream.html')


@login_required
def globalstream_action(request):
    if request.method == 'GET':
        return render(request, 'socialnetwork/globalstream.html', {})

    return render(request, 'socialnetwork/globalstream.html', {})


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
    new_post.save();
    return redirect('home')


def makecomment(request):
    if not request.user:
        return render(request, 'socialnetwork/globalstream.html', {})
    context = {'posts': Post.objects.all()}
    if 'comment' not in request.POST or not request.POST['comment']:
        context['error'] = 'You must enter an content of a comment'
        return render(request, 'socialnetwork/globalstream.html', context)

    context = {'comments': Comment.objects.all()}
    new_comment = Comment(user=request.user,
                          content=request.POST['comment'])
    new_comment.save();
    return redirect('home')

def myprofile_action(request):
    return render(request, 'socialnetwork/profile.html')


def profile_others(request):
    return render(request, 'socialnetwork/profile_others.html')


@login_required
def create_action(request):
    if request.method == 'GET':
        context = {'form': ProfileForm()}
        return render(request, 'socialnetwork/create.html', context)

    form = ProfileForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'socialnetwork/create.html', context)

    my_entry = {}
    for field in ['last_name', 'first_name', 'birthday', 'children',
                  'address', 'city', 'state', 'zip_code', 'country',
                  'email', 'phone_number']:
        my_entry[field] = form.cleaned_data[field]

    my_entry['created_by'] = request.user
    my_entry['creation_time'] = timezone.now()
    my_entry['updated_by'] = request.user
    my_entry['update_time'] = timezone.now()

    ENTRY_LIST.create(my_entry)

    message = 'Entry created'
    new_form = ProfileForm(my_entry)
    context = {'message': message, 'entry': my_entry, 'form': new_form}
    return render(request, 'socialnetwork/edit.html', context)


@login_required
def delete_action(request, id):
    if request.method != 'POST':
        message = 'Invalid request.  POST method must be used.'
        return render(request, 'socialnetwork/globalstream.html', {'message': message})

    entry = ENTRY_LIST.read(id)
    if not entry:
        context = {'message': f"Record with id={id} does not exist"}
        return render(request, 'socialnetwork/globalstream.html', context)

    message = f"Sorry, deleting is not implemented in this example."
    return render(request, 'socialnetwork/globalstream.html', {'message': message})


@login_required
def edit_action(request, id):
    entry = ENTRY_LIST.read(id)
    if not entry:
        context = {'message': f"Record with id={id} does not exist"}
        return render(request, 'socialnetwork/globalstream.html', context)

    if request.method == 'GET':
        form = ProfileForm(entry)
        context = {'entry': entry, 'form': form}
        return render(request, 'socialnetwork/edit.html', context)

    edit_form = ProfileForm(request.POST)
    if not edit_form.is_valid():
        context = {'form': edit_form, 'entry': entry}
        return render(request, 'socialnetwork/edit.html', context)

    for field in ['last_name', 'first_name', 'birthday', 'children',
                  'address', 'city', 'state', 'zip_code', 'country',
                  'email', 'phone_number']:
        entry[field] = edit_form.cleaned_data[field]

    entry['updated_by'] = request.user
    entry['update_time'] = timezone.now()

    ENTRY_LIST.update(entry)

    message = 'Entry Updated'
    context = {'message': message, 'entry': entry, 'form': edit_form}
    return render(request, 'socialnetwork/edit.html', context)


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
