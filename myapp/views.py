from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Loan
from .serializers import UserSerializer, LoanSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse


User = get_user_model()

#user registration into the system
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Custom JWT Login Serializer to return user role
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # Include user role in response
        return data
    

#user login using email and password
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#user logout
class LogoutView(APIView):    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



#Adding loans into the system
class CreateLoanView(generics.CreateAPIView):     
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#List all loans in the system for the user
class ListLoansView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)


#List all loans in the system to the Admin
class AdminListLoansView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Loan.objects.all()
        return Loan.objects.none()



#Foreclose a Loan API
class ForecloseLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, loan_id=loan_id, user=request.user)

        # Ensure total_interest and total_amount are not None
        if loan.total_interest is None or loan.total_amount is None:
            return Response(
                {"error": "Loan calculations not available."},
                status=status.HTTP_400_BAD_REQUEST
            )

        foreclosure_discount = Decimal("0.05") * loan.total_interest
        final_settlement = loan.total_amount - foreclosure_discount

        # Update loan status 
        loan.total_amount = final_settlement
        loan.status = "CLOSED"  # Add a `status` field in the Loan model if not present
        loan.save()

        return Response({
            "message": "Loan foreclosed successfully.",
            "loan_id": loan.loan_id,
            "amount_paid": float(loan.total_amount),
            "foreclosure_discount": float(foreclosure_discount),
            "final_settlement_amount": float(final_settlement),
            "status": "CLOSED"
        }, status=status.HTTP_200_OK)
    

