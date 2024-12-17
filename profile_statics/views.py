from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ProfileStatics
import calendar

class ProfileStaticsLast7DaysView(APIView):
    def get(self, request, *args, **kwargs):
        
        today = timezone.localdate()
        
        
        days = [(today - timedelta(days=i)) for i in range(7)]

        
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

            
            profile_statics = ProfileStatics.objects.filter(user__profile_statics__created_at__date=day).first()

            likes = profile_statics.likes.get(day.isoformat(), 0) if profile_statics else 0
            views = profile_statics.views.get(day.isoformat(), 0) if profile_statics else 0

            
            result.append({
                "day": persian_day_name,
                "view": views,
                "like": likes
            })

        return Response(result)
