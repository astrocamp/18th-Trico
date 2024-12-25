from django.urls import path
from . import views


app_name = "services"
urlpatterns = [
    path("<int:id>/freelancer/", views.freelancer_dashboard, name="freelancer_dashboard"),
    path("<int:id>/freelancer/<int:service_id>/detail/", views.service_detail, name="service_detail"),
    path("<int:id>/new/", views.create_service, name="create_service"),
    path("<int:id>/edit/<int:service_id>/", views.edit_service, name="edit_service"),
    path("<int:id>/delete/<int:service_id>/", views.delete_service, name="delete_service"),
    path("error/", views.error_page, name="error_page"),
]

 #services
# /ID/freelancer/
# /ID/freelancer/id/detail
# /ID/new/
# /ID/edit/id/
# /ID/delete/id/
# /error/


