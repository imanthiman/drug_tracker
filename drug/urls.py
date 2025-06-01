from django.urls import path
from .views import DrugInfoView, SideEffectsView

urlpatterns = [
    path('drug-info/', DrugInfoView.as_view(), name='drug-info'),
    path('side-effects/', SideEffectsView.as_view(), name='side-effects'),
]