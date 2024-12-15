from django.shortcuts import render


def freelancers(request, id):
    return render(request, "freelancers/freelancers.html", {"id": id})
