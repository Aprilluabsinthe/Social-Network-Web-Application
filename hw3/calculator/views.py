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


def update(a, b):
    return int(float(a)) * 10 + int(b)


def home_page(request):
    context = {}
    context['prev_opr'] = "plus"
    context['prev_val'] = '0'
    context['new_val'] = '0'
    context['cal_result'] = '0'
    return render(request, 'calculator/calculator.html', context)

def isnum(s):
    try:
        float(s)
    except:
        return False
    else:
        return True

def calculator(request):
    errors = []
    context = {}
    if 'prev_opr' not in request.POST or request.POST['prev_opr'] not in ['plus', 'minus', 'times', 'divide']:
        errors.append("Operation Error: Previous Operator changed or deleted")
    if 'prev_val' not in request.POST or not isnum(request.POST['prev_val']):
        errors.append("ValueError: Previous Value changed or deleted")
    if 'new_val' not in request.POST or not isnum(request.POST['new_val']):
        errors.append("ValueError: New Value changed or deleted")
    if 'button' not in request.POST or request.POST['button'] not in ([chr(x) for x in range(48, 58)] + ['plus', 'minus', 'times', 'divide','equals']):
        errors.append("ValueError: no button clicked or button value changed")
    if errors:
        return render(request, 'calculator/calculator.html', {'errors': errors})

    prev_opr = request.POST['prev_opr']
    prev_val = request.POST['prev_val']
    new_val = request.POST['new_val']
    buttonvalue = request.POST['button']

    if buttonvalue in [chr(x) for x in range(48, 58)]:
        update_val = str(update(new_val, buttonvalue))
        context['prev_opr'] = prev_opr
        context['prev_val'] = prev_val
        context['new_val'] = update_val
        context['cal_result'] = update_val
        context['errors'] = errors
        return render(request, 'calculator/calculator.html', context)
    else:  # operations
        try:
            if prev_opr == 'plus':
                cal_result = plus(prev_val, new_val)
            elif prev_opr == 'minus':
                cal_result = minus(prev_val, new_val)
            elif prev_opr == 'times':
                cal_result = times(prev_val, new_val)
            elif prev_opr == 'divide':
                cal_result = divide(prev_val, new_val)
            else:
                errors.append("Operation Value: previous operation changed")
                return render(request, 'calculator/calculator.html', {'errors': errors})

            if buttonvalue in ['plus', 'minus', 'times', 'divide']:
                prev_opr = buttonvalue
                prev_val = str(cal_result)
                new_val = '0'
            elif buttonvalue == 'equals':
                prev_opr = 'plus'
                prev_val = '0'
                new_val = '0'
            else:
                errors.append("Button invalid: button value changed")
                return render(request, 'calculator/calculator.html', {'errors': errors})
            # renew memories
            context['prev_opr'] = prev_opr
            context['prev_val'] = prev_val
            context['new_val'] = new_val
            context['cal_result'] = str(cal_result)
            context['errors'] = errors
            return render(request, 'calculator/calculator.html', context)
        except ZeroDivisionError as error:
            errors.append("ZeroDivisionError : Can not divide 0")
            return render(request, 'calculator/calculator.html', {'errors': errors})
