from django.urls import path
from .views import (
    InvestmentCreateView, 
    InvestmentHistoryView, 
    ProjectInvestmentHistoryView,
    StartupInvestmentHistoryView
)

urlpatterns = [
    path("create_investment/<int:position_id>/", InvestmentCreateView.as_view(), name="create_investment"),
    path("history/<str:username>/<str:sort>/", InvestmentHistoryView.as_view(), name="investment_history"),
    path("history/project/<int:project_id>/<str:sort>/", ProjectInvestmentHistoryView.as_view(), name="project_investment_history"),
    path("history/startup/<int:startup_id>/<str:sort>/", StartupInvestmentHistoryView.as_view(), name="startup_investment_history"),
]
