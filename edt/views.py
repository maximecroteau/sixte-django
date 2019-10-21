import datetime
from django.shortcuts import render
from edt import function
from .forms import DateForm


def index(request):
    form_class = DateForm
    form = form_class(request.POST or None)

    daterequest = datetime.datetime.today().strftime('%m/%d/%Y')

    if request.method == 'POST':
        if form.is_valid():
            daterequest = form.cleaned_data['date']
            daterequest = datetime.datetime.strftime(daterequest, '%m/%d/%Y')

    lst = function.scrap(daterequest)

    today = lst[0]
    lundi = lst[1]
    mardi = lst[2]
    mercredi = lst[3]
    jeudi = lst[4]
    vendredi = lst[5]

    print(lundi)
    print(mardi)
    print(mercredi)
    print(jeudi)
    print(vendredi)

    return render(request, 'menu/edt.html', {
        "today": today,
        "lundi": lundi,
        "mardi": mardi,
        "mercredi": mercredi,
        "jeudi": jeudi,
        "vendredi": vendredi,
        "form": form,
    })
