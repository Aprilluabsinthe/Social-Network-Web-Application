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


def calculator(request):
    errors = []
    if 'prev_opr' not in request.session:
        errors.append("Error: Must Have Previous Operator")
    if 'prev_val' not in request.session:
        errors.append("Error: Must Have Previous Value")
    if 'new_val' not in request.session:
        errors.append("Error: Must Have New Value")
    context = {}
    prev_opr = request.session['prev_opr']
    prev_val = request.session['prev_val']
    new_val = request.session['new_val']
    if 'button' in request.GET:
        buttonvalue = request.GET['button']
        if buttonvalue in [chr(x) for x in range(48,58)]:
            update_val = str(update(new_val,buttonvalue))
            request.session['new_val'] = update_val
            context['prev_opr'] = prev_opr
            context['prev_val'] = prev_val
            context['new_val'] = update_val
            context['cal_result'] = update_val
            context['errors'] = errors
            return render(request, 'calculator/calculator.html', context)
        else: # operations
            try:
                if prev_opr == 'plus':
                    cal_result = plus(prev_val,new_val)
                elif prev_opr == 'minus':
                    cal_result = minus(prev_val, new_val)
                elif prev_opr == 'times':
                    cal_result = times(prev_val, new_val)
                elif prev_opr == 'divide':
                    cal_result = divide(prev_val, new_val)
                if buttonvalue in ['plus', 'minus', 'times', 'divide']:
                    request.session['prev_opr'] = buttonvalue
                    request.session['prev_val'] = str(cal_result)
                    request.session['new_val'] = '0'
                else:
                    request.session['prev_opr'] = 'plus'
                    request.session['prev_val'] = '0'
                    request.session['new_val'] = '0'
                context['prev_opr'] = request.session['prev_opr']
                context['prev_val'] = request.session['prev_val']
                context['new_val'] =  request.session['new_val']
                context['cal_result'] = str(cal_result)
                context['errors'] = errors
                return render(request, 'calculator/calculator.html', context)
            except ZeroDivisionError as error:
                errors.append("ZeroDivisionError : Can not divide 0")
                return render(request, 'calculator/calculator.html', {'errors':errors})
    errors.append("Error: Please click on Valid Buttons")
    context['errors'] = errors
    return render(request, 'calculator/calculator.html', {'errors': errors})
