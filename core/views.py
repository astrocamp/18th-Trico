from django.shortcuts import render

def vue404_page(request):
    return render(request, 'shared/vue404_page.html')
