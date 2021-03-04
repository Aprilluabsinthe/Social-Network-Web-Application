from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import ProfileForm, LoginForm, RegisterForm

from socialnetwork.MyMemoryList import MyMemoryList

ENTRY_LIST = MyMemoryList()


@login_required
def followerstream_action(request):
    return render(request, 'socialnetwork/followerstream.html')


@login_required
def globalstream_action(request):
    if 'last' not in request.GET:
        return render(request, 'socialnetwork/globalstream.html', {})

    last = request.GET['last'].lower()
    if len(last) != 1:
        message = f"Invalid value for last: {last}"
        return render(request, 'socialnetwork/globalstream.html', {'message': message})
        return render(request, 'socialnetwork/globalstream.html', {'message': message})

    matches = ENTRY_LIST.match(last)

    if len(matches) == 0:
        message = 'No entries with last name = "{0}"'.format(last)
        return render(request, 'socialnetwork/globalstream.html', {'message': message})

    if len(matches) == 1:
        match = matches[0]
        form = ProfileForm(match)
        context = {'entry': match, 'form': form}
        return render(request, 'socialnetwork/edit.html', context)

    context = {'entries': matches}
    return render(request, 'socialnetwork/list.html', context)


def profile_action(request):
    return render(request, 'socialnetwork/profile.html')
    # if request.method == 'GET':
    #     context = {'form': ProfileForm()}
    #     return render(request, 'socialnetwork/profile.html', context)
    #
    # form = ProfileForm(request.POST)
    # if not form.is_valid():
    #     context = {'form': form}
    #     return render(request, 'addrbook/create.html', context)
    #
    # my_entry = {}
    # for field in ['last_name', 'first_name', 'birthday', 'children',
    #               'address', 'city', 'state', 'zip_code', 'country',
    #               'email', 'phone_number']:
    #     my_entry[field] = form.cleaned_data[field]
    #
    # my_entry['created_by'] = request.user
    # my_entry['creation_time'] = timezone.now()
    # my_entry['updated_by'] = request.user
    # my_entry['update_time'] = timezone.now()
    #
    # ENTRY_LIST.create(my_entry)
    #
    # message = 'Entry created'
    # new_form = ProfileForm(my_entry)
    # context = {'message': message, 'entry': my_entry, 'form': new_form}
    # return render(request, 'addrbook/edit.html', context)
    return render(request, 'socialnetwork/profile.html')


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
