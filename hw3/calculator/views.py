from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def plus(a, b):
    return int(float(a)) + int(float(b))


def minus(a, b):
    return int(float(a)) - int(float(b))


def times(a, b):
    return int(float(a)) * int(float(b))


def divide(a, b):
    return int(int(float(a)) / int(float(b)))

def update(a,b):
    return int(float(a)) * 10 + int(b)

def home_page(request):
    request.session.set_test_cookie()
    context = {}
    request.session['prev_opr'] = "plus"
    request.session['prev_val'] = '0'
    request.session['new_val'] = '0'
    context['prev_opr'] = "plus"
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
    prev_opr = request.session['prev_opr']
    prev_val = request.session['prev_val']
    new_val = request.session['new_val']
    if 'button' in request.GET:
        buttonvalue = request.GET['button']
        if buttonvalue in ['0','1','2','3','4','5','6','7','8','9']:
            update_val = str(update(new_val,buttonvalue))
            request.session['prev_opr'] = request.GET['prev_opr']
            request.session['prev_val'] = request.GET['prev_val']
            request.session['new_val'] = update_val
            context['prev_opr'] = prev_opr
            context['prev_val'] = prev_val
            context['new_val'] = update_val
            context['cal_result'] = update_val
            return render(request, 'calculator/calculator.html', context)
        elif buttonvalue in ['plus','minus','times','divide']:
            if prev_opr == 'plus':
                cal_result = plus(prev_val,new_val)
            elif prev_opr == 'minus':
                cal_result = minus(prev_val, new_val)
            elif prev_opr == 'times':
                cal_result = times(prev_val, new_val)
            elif prev_opr == 'divide':
                cal_result = divide(prev_val, new_val)
            request.session['prev_opr'] = buttonvalue
            request.session['prev_val'] = str(cal_result)
            request.session['new_val'] = '0'
            context['prev_opr'] = request.session['prev_opr']
            context['prev_val'] = request.session['prev_val']
            context['new_val'] =  request.session['new_val']
            context['cal_result'] = str(cal_result)
            return render(request, 'calculator/calculator.html', context)