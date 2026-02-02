from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.BloodRequestCreateView.as_view(), name="blood-request-create"),
    path("list/", views.BloodRequestListView.as_view(), name="blood-request-list"),
    path("<int:pk>/", views.BloodRequestDetailView.as_view(), name="blood-request-detail"),
]


