from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def plus(a, b):
    return int(a) + int(b)


def minus(a, b):
    return int(a) - int(b)


def multiple(a, b):
    return int(a) * int(b)


def divide(a, b):
    return int(int(a) / int(b))


def home_page(request):
    context = {}
    context['prev_opr'] = '+'
    context['prev_val'] = '0'
    context['new_val'] = '0'
    context['cal_result'] = '0'
    return render(request, 'calculator/calculator.html', context)

# def do_calculation(request):
#     context = {}
#     if 'opr' in request.GET:
#         if request.GET['opr'] == '+':
#             prev_val = request.GET['calc_result']
#             new_val = '0'
#             context['prev_opr'] = '&/plus;'
#             context['prev_val'] = request.GET['calc_result']
#             context['new_val'] = '0'
#             context['calc_result'] = plus(prev_val,new_val)
#             return render(request,'calculator/calculator.html',context)
#     return render(request, 'calculator/calculator.html', context)

# def setNum(request):
#     # if 'num' in request.POST:
#     new_val = request.POST['button']
#     context = {}
#     context['prev_opr'] = '+'
#     context['prev_val'] = '0'
#     context['new_val'] = '0'
#     context['cal_result'] = new_val
#     return render(request, 'calculator/calculator.html', context)

def calculator(request):
    context = {}
    # if 'button' in request.session:
    new_val = request.POST['button']
    context = {}
    context['prev_opr'] = '+'
    context['prev_val'] = '0'
    context['new_val'] = new_val
    context['cal_result'] = new_val
    return render(request, 'calculator/calculator.html', context)