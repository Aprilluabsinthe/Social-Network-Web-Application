from django.shortcuts import render
from calculator.forms import EntryForm


# Create your views here.
def home(request):
    context = {'form': EntryForm()}
    return render(request, 'calculator/index.html', context)


def calculator(request):
    if request.method == 'GET':
        context = {'form': EntryForm()}
        return render(request, 'calculator/index.html', context)

    form = EntryForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'calculator/index.html', context)

    x = form.cleaned_data['x']
    y = form.cleaned_data['y']
    result = x / y
    message = f"{x} / {y} = {result}"
    context = {'form': EntryForm(), 'message': message}
    return render(request, 'calculator/index.html', context)
