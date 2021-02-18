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
    if errors:
        return render(request, 'calculator/calculator.html', {'errors': errors})
    context = {}
    try:
        prev_opr = request.session['prev_opr']
        prev_val = request.session['prev_val']
        new_val = request.session['new_val']
    except:
        errors.append("Session Error: Session be changed")
        return render(request, 'calculator/calculator.html', {'errors': errors})

    if 'button' not in request.GET:
        errors.append("ValueError: no button clicked")
    if 'prev_opr' not in request.GET or request.GET['prev_opr'] not in ['plus', 'minus', 'times', 'divide']:
        errors.append("Operation Error: Previous Operator changed or deleted")
    if 'prev_val' not in request.GET or not request.GET['prev_val'].isnumeric():
        errors.append("ValueError: Previous Value changed or deleted")
    if 'new_val' not in request.GET or not request.GET['new_val'].isnumeric():
        errors.append("ValueError: New Value changed or deleted")
        return render(request, 'calculator/calculator.html', {'errors': errors})

    else:
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
                else:
                    errors.append("Operation Value: previous operation changed")
                    return render(request, 'calculator/calculator.html', {'errors': errors})

                if buttonvalue in ['plus', 'minus', 'times', 'divide']:
                    request.session['prev_opr'] = buttonvalue
                    request.session['prev_val'] = str(cal_result)
                    request.session['new_val'] = '0'
                elif buttonvalue == 'equals':
                    request.session['prev_opr'] = 'plus'
                    request.session['prev_val'] = '0'
                    request.session['new_val'] = '0'
                else:
                    errors.append("Button invalid: button value changed")
                    return render(request, 'calculator/calculator.html', {'errors': errors})
                # renew sessions
                context['prev_opr'] = request.session['prev_opr']
                context['prev_val'] = request.session['prev_val']
                context['new_val'] =  request.session['new_val']
                context['cal_result'] = str(cal_result)
                context['errors'] = errors
                return render(request, 'calculator/calculator.html', context)
            except ZeroDivisionError as error:
                errors.append("ZeroDivisionError : Can not divide 0")
                return render(request, 'calculator/calculator.html', {'errors':errors})
