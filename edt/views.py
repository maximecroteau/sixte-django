import datetime
from django.shortcuts import render
from edt import function
from .forms import DateForm


def index(request):
    form_class = DateForm
    form = form_class(request.POST or None)

    daterequest = datetime.datetime.today().strftime('%m/%d/%Y')

    if request.method == 'POST':
        print('before valid')
        if form.is_valid():
            print('valid')
            daterequest = form.cleaned_data['date']
            print(daterequest)
            daterequest = datetime.datetime.strftime(daterequest, '%m/%d/%Y')
            print(daterequest)

    lst = function.scrap(daterequest)

    return render(request, 'menu/edt.html', {
        "lst": lst,
        "form": form,
    })
