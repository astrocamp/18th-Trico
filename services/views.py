from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
from .models import Category



def has_permission(request, id):
    print(f"Checking permission for User ID: {request.user.id}, Requested ID: {id}")
    return request.user.id == id


@login_required
def freelancer_dashboard(request, id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    freelancer = request.user  
    
    services = (
        Service.objects.prefetch_related("comments")
        .filter(freelancer_user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "services/freelancer_dashboard.html",
        {
            "freelancer": freelancer,
            "services": services,
        },
    )


@login_required
def create_service(request, id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    categories = Category.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer_user = request.user
            service.save()
            return redirect("services:freelancer_dashboard", id=id)
    else:
        form = ServiceForm()

    return render(
        request,
        "services/create_service.html",
        {"form": form, "categories": categories},
    )



@login_required
def edit_service(request, id, service_id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    service = get_object_or_404(Service, id=service_id, freelancer_user=request.user)

    categories = Category.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect("services:freelancer_dashboard", id=id)
    else:
        form = ServiceForm(instance=service)

    return render(
        request, "services/edit_service.html", {"form": form, "categories": categories}
    )


@login_required
def delete_service(request, id, service_id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    service = get_object_or_404(Service, id=service_id, freelancer_user=request.user)

    if request.method == "POST":
        service.delete()
        return redirect("services:freelancer_dashboard", id=id)

    return render(
        request, "services/delete_service.html", {"service": service, "id": id}
    )


def error_page(request):
    return render(
        request,
        "services/error_page.html",
        {"message": "You do not have permission to view this page."},
    )
