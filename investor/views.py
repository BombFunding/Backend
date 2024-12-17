# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Investor
# from .serializers import InvestorSerializer
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# class InvestorUpdateView(APIView):
#     permission_classes = [IsAuthenticated]  

    
#     @swagger_auto_schema(
#         operation_description="Retrieve investor profile without authentication.",
#         responses={
#             200: openapi.Response(
#                 description="Investor details",
#                 examples={
#                     "application/json": {
#                         "id": 1,
#                         "name": "Investor A",
#                         "tax_identification_number": "123456789",
#                         "contact_number": "+989123456789",
#                         "investor_ending_date": "2025-12-31",
#                         "address": "123 Investor Street",
#                         "starting_date": "2022-01-01"
#                     }
#                 }
#             ),
#             404: openapi.Response(
#                 description="Investor not found",
#                 examples={"application/json": {"detail": "Investor not found."}},
#             ),
#         }
#     )
#     def get(self, request, investor_id):
#         try:
#             investor = Investor.objects.get(pk=investor_id)
#         except Investor.DoesNotExist:
#             return Response({"detail": "Investor not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = InvestorSerializer(investor)
#         return Response(serializer.data, status=status.HTTP_200_OK)

    
#     @swagger_auto_schema(
#         operation_description="Update investor profile.",
#         request_body=InvestorSerializer,
#         responses={
#             200: openapi.Response(
#                 description="Investor updated successfully",
#                 examples={
#                     "application/json": {
#                         "id": 1,
#                         "name": "Investor A",
#                         "tax_identification_number": "123456789",
#                         "contact_number": "+989123456789",
#                         "investor_ending_date": "2025-12-31",
#                         "address": "123 Investor Street"
#                     }
#                 }
#             ),
#             404: openapi.Response(
#                 description="Investor not found",
#                 examples={"application/json": {"detail": "Investor not found."}},
#             ),
#             400: openapi.Response(
#                 description="Invalid data",
#                 examples={"application/json": {"detail": "Invalid data."}},
#             ),
#         }
#     )
#     def post(self, request, investor_id):
#         try:
#             investor = Investor.objects.get(pk=investor_id)
#         except Investor.DoesNotExist:
#             return Response({"detail": "Investor not found."}, status=status.HTTP_404_NOT_FOUND)

        
#         if request.user != investor.user:
#             return Response({"detail": "You can only update your own profile."}, status=status.HTTP_403_FORBIDDEN)
        
        
#         if 'starting_date' in request.data:
#             del request.data['starting_date']
        
#         serializer = InvestorSerializer(instance=investor, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
