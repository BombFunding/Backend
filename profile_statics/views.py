from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ProfileStatics
import calendar
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProfileStaticsLast7DaysView(APIView):
    
    @swagger_auto_schema(
        operation_description="Get statistics (views and likes) for the last 7 days.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of statistics for the last 7 days",
                examples={
                    'application/json': [
                        {"day": "دوشنبه", "view": 10, "like": 5},
                        {"day": "یک‌شنبه", "view": 8, "like": 4},
                        {"day": "شنبه", "view": 0, "like": 0},
                        {"day": "جمعه", "view": 15, "like": 8},
                        {"day": "پنج‌شنبه", "view": 10, "like": 6},
                        {"day": "چهارشنبه", "view": 9, "like": 4},
                        {"day": "سه‌شنبه", "view": 11, "like": 3}
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        
        today = timezone.localdate()
        
        
        days = [(today - timedelta(days=i)) for i in range(7)]
        
        
        username = request.GET.get("username", None)
        
        result = []
        
        for day in days:
            
            day_name = calendar.day_name[day.weekday()]
            persian_day_names = {
                "Monday": "یک‌شنبه",
                "Tuesday": "دوشنبه",
                "Wednesday": "سه‌شنبه",
                "Thursday": "چهارشنبه",
                "Friday": "پنج‌شنبه",
                "Saturday": "جمعه",
                "Sunday": "شنبه",
            }
            persian_day_name = persian_day_names.get(day_name, day_name)
            
            
            if username:
                profile_statics = ProfileStatics.objects.filter(user__username=username).first()
            else:
                profile_statics = ProfileStatics.objects.first()

            
            likes = profile_statics.likes.get(day.isoformat(), 0) if profile_statics else 0
            views = profile_statics.views.get(day.isoformat(), 0) if profile_statics else 0

            
            result.append({
                "day": persian_day_name,
                "view": views,
                "like": likes
            })

        return Response(result)
