from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ProfileStatics
import calendar
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from calendar import month_name
from django.utils.timezone import now
from position.models import Position , Transaction
from django.db.models import Sum
from django.utils import timezone

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
        
        
        days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  
        
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


from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from django.utils.timezone import now
import jdatetime


class ProfileStaticsLast6MonthsView(APIView):
    
    @swagger_auto_schema(
        operation_description="Get fund statistics for the last 6 months for a specific startup.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, 
                description="Username of the startup to filter the statistics by", 
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last 6 months",
                examples={
                    'application/json': [
                        {"month": "آبان", "fund": "100000"},
                        {"month": "مهر", "fund": "75000"},
                        {"month": "شهریور", "fund": "120000"},
                        {"month": "مرداد", "fund": "50000"},
                        {"month": "تیر", "fund": "85000"},
                        {"month": "خرداد", "fund": "95000"}
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        
        # today = jdatetime.date.today()
        today = timezone.datetime.now()
        today = jdatetime.datetime.fromgregorian(date=timezone.now())
        current_month = today.replace(day=1, hour=0, minute=0, second=0)

        
        positions = Position.objects.filter(position_user__username=username)
        if not positions.exists():
            return Response({"error": "No positions found for this startup."}, status=404)

        
        result = []
        for i in range(6):
            month_date = (current_month - timedelta(days=1)).replace(day=1) if i > 0 else current_month
            current_month = month_date.replace(day=1)

            persian_month_names = {
                1: "فروردین", 2: "اردیبهشت", 3: "خرداد",
                4: "تیر", 5: "مرداد", 6: "شهریور",
                7: "مهر", 8: "آبان", 9: "آذر",
                10: "دی", 11: "بهمن", 12: "اسفند",
            }
            
            month_name_persian = persian_month_names.get(month_date.month, str(month_date.month))

            gregorian_start_date = (month_date.togregorian())
            print(gregorian_start_date)
            gregorian_end_date = ((month_date + jdatetime.timedelta(days=30)).togregorian())
            print(gregorian_end_date)
            
            monthly_transactions = Transaction.objects.filter(
                position__in=positions,
                investment_date__gte=gregorian_start_date,
                investment_date__lt=gregorian_end_date,
            )

            total_fund = monthly_transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "month": month_name_persian,
                "fund": f"{total_fund:.0f}"
            })

        
        return Response(result[::-1])