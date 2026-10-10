from django.shortcuts import render


def home(request):
    context = {
        "page_title": "DataPulse",
        "page_subtitle": "Inteligência de vendas para e-commerce",
    }

    return render(request, "dashboard/home.html", context)
