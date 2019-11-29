from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, 'web/COLI_main.html', {})

def main_page2(request):
    return render(request, 'web/main2.html', {})

def main_page3(request):
    return render(request, 'web/main3.html', {})
