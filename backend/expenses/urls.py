from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expenses.views import (
    LoginView, AuthStatusView, GroupViewSet, MembershipView,
    GroupExpensesView, GroupSettlementsView, GroupBalancesView,
    ImportParseView, ImportConfirmView, ImportListView, ImportReportView,
    GroupAnalyticsView, api_root_view,
    AIGenerateInsightsView, AIGenerateImportSummaryView
)

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', api_root_view, name='api_root'),
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/status/', AuthStatusView.as_view(), name='auth_status'),
    path('api/groups/<int:group_id>/members/', MembershipView.as_view(), name='group_members'),
    path('api/groups/<int:group_id>/expenses/', GroupExpensesView.as_view(), name='group_expenses'),
    path('api/groups/<int:group_id>/expenses/<int:pk>/', GroupExpensesView.as_view(), name='group_expense_detail'),
    path('api/groups/<int:group_id>/settlements/', GroupSettlementsView.as_view(), name='group_settlements'),
    path('api/groups/<int:group_id>/settlements/<int:pk>/', GroupSettlementsView.as_view(), name='group_settlement_detail'),
    path('api/groups/<int:group_id>/balances/', GroupBalancesView.as_view(), name='group_balances'),
    path('api/groups/<int:group_id>/analytics/', GroupAnalyticsView.as_view(), name='group_analytics'),
    path('api/groups/<int:group_id>/import/parse/', ImportParseView.as_view(), name='import_parse'),
    path('api/groups/<int:group_id>/import/confirm/', ImportConfirmView.as_view(), name='import_confirm'),
    path('api/groups/<int:group_id>/imports/', ImportListView.as_view(), name='import_list'),
    path('api/groups/<int:group_id>/imports/<int:import_id>/report/', ImportReportView.as_view(), name='import_report'),
    path('api/groups/<int:group_id>/ai/insights/', AIGenerateInsightsView.as_view(), name='ai_insights'),
    path('api/groups/<int:group_id>/ai/import-summary/<int:import_id>/', AIGenerateImportSummaryView.as_view(), name='ai_import_summary'),
]
