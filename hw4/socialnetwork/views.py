from django.shortcuts import render


# Create your views here.
def base(request):
    context['new_val'] = '0'
    context['cal_result'] = '0'
    return render(request, base)
