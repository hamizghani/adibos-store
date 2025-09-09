from django.shortcuts import render

def show_main(request):
    context = {
        'app_name' : 'Adibos Store',
        'name': 'Muhammad Hmaiz Ghani Ayusha',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)