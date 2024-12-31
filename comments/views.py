from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from services.models import Service

@login_required
def add_comment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.service = service
            comment.save()
            return redirect('services:freelancer_dashboard', id=request.user.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form, 'service': service})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('services:freelancer_dashboard', id=request.user.id)
    return render(request, 'comments/delete_comment.html', {'comment': comment})


@login_required
def feedback_view(request):
    comments_given = Comment.objects.filter(user=request.user).order_by(
        "-created_at"
    )  
    comments_received = Comment.objects.filter(
        service__freelancer_user=request.user
    ).order_by(
        "-created_at"
    )  
    return render(
        request,
        "users/feedback.html",
        {
            "comments_given": comments_given,
            "comments_received": comments_received,
        },
    )
