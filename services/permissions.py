def has_permission(request, id):
    return str(request.user.id) == str(id)
