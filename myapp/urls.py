from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, CreateLoanView, ListLoansView, AdminListLoansView, ForecloseLoanView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # JWT Login
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('loans/', ListLoansView.as_view(), name='list_loans'),
    path('loans/add/', CreateLoanView.as_view(), name='add_loan'),
    path('loans/all/', AdminListLoansView.as_view(), name='admin_list_loans'),
    path('loans/<str:loan_id>/foreclose/', ForecloseLoanView.as_view(), name='foreclose_loan'),
]
