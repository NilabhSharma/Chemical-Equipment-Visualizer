from django.urls import path

from equipment.views import UploadCSVView, HistoryView, HomeView, download_report

urlpatterns = [
    path("", HomeView.as_view()),
    path("upload/", UploadCSVView.as_view()),
    path("history/", HistoryView.as_view()),
    path("report/<int:dataset_id>/", download_report),
]
