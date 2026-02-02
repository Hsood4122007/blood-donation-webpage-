from django.urls import path

from . import views

urlpatterns = [
    path("stats/", views.SystemStatsView.as_view(), name="analytics-stats"),
    path(
        "donor-distribution/",
        views.DonorDistributionView.as_view(),
        name="analytics-donor-distribution",
    ),
    path(
        "monthly-trends/",
        views.MonthlyTrendsView.as_view(),
        name="analytics-monthly-trends",
    ),
]


