from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.utils import timezone
import calendar
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from invest.models import Transaction
from django.db.models import Sum
from project.models import Project
from profile_statics.models import ProjectStatistics
from rest_framework import status

class ProjectStatisticsLast7DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get statistics (views and likes) for the last 7 days for all projects of a user.",
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
        """
        Fetch statistics (views and likes) for the last 7 days for all projects of a user.
        """
        today = timezone.localdate()
        days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        result = []

        for day in days:
            day_name = calendar.day_name[day.weekday()]
            persian_day_names = {
                "Monday": "دوشنبه",
                "Tuesday": "سه‌شنبه",
                "Wednesday": "چهارشنبه",
                "Thursday": "پنج‌شنبه",
                "Friday": "جمعه",
                "Saturday": "شنبه",
                "Sunday": "یک‌شنبه",
            }
            persian_day_name = persian_day_names.get(day_name, day_name)

            total_views = 0
            total_likes = 0

            for project in projects:
                project_statics = ProjectStatistics.objects.filter(project=project).first()
                if project_statics:
                    total_views += project_statics.views.get(day.isoformat(), 0)
                    total_likes += len(project_statics.likes.get(day.isoformat(), []))

            result.append({
                "day": persian_day_name,
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class ProjectStatisticsLast6MonthsView(APIView):

    @swagger_auto_schema(
        operation_description="Get fund statistics for the last 6 months for all projects of a user.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, 
                description="Username to filter the statistics by", 
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
        """
        Fetch fund statistics for the last 6 months for all projects of a user.
        """
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now()
        current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

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

            start_date = month_date
            end_date = (month_date + timedelta(days=30))

            monthly_transactions = Transaction.objects.filter(
                position__project__in=projects,
                investment_date__gte=start_date,
                investment_date__lt=end_date,
            )

            total_fund = monthly_transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "month": month_name_persian,
                "fund": f"{total_fund:.0f}"
            })

        return Response(result[::-1])


class ProjectVisitView(APIView):
    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            
            # Check if visitor is not the project owner
            if request.user == project.user:
                return Response(
                    {"error": "Project owner cannot visit their own project"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get or create project statistics
            stats, _ = ProjectStatistics.objects.get_or_create(project=project)
            stats.increment_view()

            return Response({"message": "Visit recorded successfully"}, status=status.HTTP_200_OK)
            
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ProjectVisitCountView(APIView):
    @swagger_auto_schema(
        operation_description="Get total visit count for a project",
        responses={
            200: openapi.Response(
                description="Visit count",
                examples={
                    'application/json': {
                        'visit_count': 42
                    }
                }
            )
        }
    )
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            stats = ProjectStatistics.objects.get_or_create(project=project)[0]
            
            return Response({
                "visit_count": stats.get_total_visits()
            }, status=status.HTTP_200_OK)
            
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class StartupVisitCountView(APIView):
    @swagger_auto_schema(
        operation_description="Get total visit count for all projects owned by a startup",
        responses={
            200: openapi.Response(
                description="Total visit count for startup's projects",
                examples={
                    'application/json': {
                        'visit_count': 150
                    }
                }
            )
        }
    )
    def get(self, request, startup_id):
        try:
            # Get all projects owned by the startup
            projects = Project.objects.filter(owner_id=startup_id)
            
            if not projects.exists():
                return Response(
                    {"error": "No projects found for this startup"},
                    status=status.HTTP_404_NOT_FOUND
                )

            total_visits = 0
            for project in projects:
                stats = ProjectStatistics.objects.get_or_create(project=project)[0]
                total_visits += stats.get_total_visits()

            return Response({
                "visit_count": total_visits
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": "Startup not found or invalid ID"},
                status=status.HTTP_404_NOT_FOUND
            )


class StartupStatisticsLast30DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for all projects of a startup for the last 30 days.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of statistics for the last 30 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(30)]

        result = []

        for day in days:
            total_views = 0
            total_likes = 0

            for project in projects:
                project_statics = ProjectStatistics.objects.filter(project=project).first()
                if project_statics:
                    total_views += project_statics.views.get(day.isoformat(), 0)
                    total_likes += len(project_statics.likes.get(day.isoformat(), []))

            result.append({
                "date": day.isoformat(),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class StartupStatisticsLast90DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for all projects of a startup for the last 90 days.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of statistics for the last 90 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(90)]

        result = []

        for day in days:
            total_views = 0
            total_likes = 0

            for project in projects:
                project_statics = ProjectStatistics.objects.filter(project=project).first()
                if project_statics:
                    total_views += project_statics.views.get(day.isoformat(), 0)
                    total_likes += len(project_statics.likes.get(day.isoformat(), []))

            result.append({
                "date": day.isoformat(),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class StartupStatisticsLastYearView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for all projects of a startup for the last year (monthly).",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of statistics for the last year",
                examples={
                    'application/json': [
                        {"month": "2024-01", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        months = [(today.replace(day=1) - timedelta(days=i*30)).replace(day=1) for i in range(12)]

        result = []

        for month in months:
            total_views = 0
            total_likes = 0

            for project in projects:
                project_statics = ProjectStatistics.objects.filter(project=project).first()
                if project_statics:
                    for day in range(1, calendar.monthrange(month.year, month.month)[1] + 1):
                        date_str = month.replace(day=day).isoformat()
                        total_views += project_statics.views.get(date_str, 0)
                        total_likes += len(project_statics.likes.get(date_str, []))

            result.append({
                "month": month.strftime("%Y-%m"),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class ProjectStatisticsLast30DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for a specific project for the last 30 days.",
        responses={
            200: openapi.Response(
                description="A list of statistics for the last 30 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(30)]

        result = []

        for day in days:
            project_statics = ProjectStatistics.objects.filter(project=project).first()
            total_views = project_statics.views.get(day.isoformat(), 0) if project_statics else 0
            total_likes = len(project_statics.likes.get(day.isoformat(), [])) if project_statics else 0

            result.append({
                "date": day.isoformat(),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class ProjectStatisticsLast90DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for a specific project for the last 90 days.",
        responses={
            200: openapi.Response(
                description="A list of statistics for the last 90 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(90)]

        result = []

        for day in days:
            project_statics = ProjectStatistics.objects.filter(project=project).first()
            total_views = project_statics.views.get(day.isoformat(), 0) if project_statics else 0
            total_likes = len(project_statics.likes.get(day.isoformat(), [])) if project_statics else 0

            result.append({
                "date": day.isoformat(),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class ProjectStatisticsLastYearView(APIView):

    @swagger_auto_schema(
        operation_description="Get total likes and views for a specific project for the last year (monthly).",
        responses={
            200: openapi.Response(
                description="A list of statistics for the last year",
                examples={
                    'application/json': [
                        {"month": "2024-01", "like": "4234", "view": "234"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        months = [(today.replace(day=1) - timedelta(days=i*30)).replace(day=1) for i in range(12)]

        result = []

        for month in months:
            total_views = 0
            total_likes = 0

            project_statics = ProjectStatistics.objects.filter(project=project).first()
            if project_statics:
                for day in range(1, calendar.monthrange(month.year, month.month)[1] + 1):
                    date_str = month.replace(day=day).isoformat()
                    total_views += project_statics.views.get(date_str, 0)
                    total_likes += len(project_statics.likes.get(date_str, []))

            result.append({
                "month": month.strftime("%Y-%m"),
                "view": total_views,
                "like": total_likes
            })

        return Response(result)


class StartupFundStatisticsLast30DaysView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        operation_description="Get total fund for all projects of a startup for the last 30 days.",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last 30 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(30)]

        result = []

        for day in days:
            total_fund = 0

            for project in projects:
                transactions = Transaction.objects.filter(
                    position__project=project,
                    investment_date__date=day
                )
                total_fund += transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "date": day.isoformat(),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)


class StartupFundStatisticsLast90DaysView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        operation_description="Get total fund for all projects of a startup for the last 90 days.",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last 90 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(90)]

        result = []

        for day in days:
            total_fund = 0

            for project in projects:
                transactions = Transaction.objects.filter(
                    position__project=project,
                    investment_date__date=day
                )
                total_fund += transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "date": day.isoformat(),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)


class StartupFundStatisticsLastYearView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username to filter the statistics by", type=openapi.TYPE_STRING
            ),
        ],
        operation_description="Get total fund for all projects of a startup for the last year (monthly).",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last year",
                examples={
                    'application/json': [
                        {"month": "2024-01", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", None)
        if not username:
            return Response({"error": "Username is required."}, status=400)

        projects = Project.objects.filter(user__username=username)
        if not projects.exists():
            return Response({"error": "No projects found for this user."}, status=404)

        today = timezone.now().date()
        months = [(today.replace(day=1) - timedelta(days=i*30)).replace(day=1) for i in range(12)]

        result = []

        for month in months:
            total_fund = 0

            for project in projects:
                transactions = Transaction.objects.filter(
                    position__project=project,
                    investment_date__year=month.year,
                    investment_date__month=month.month
                )
                total_fund += transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "month": month.strftime("%Y-%m"),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)


class ProjectFundStatisticsLast30DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total fund for a specific project for the last 30 days.",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last 30 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(30)]

        result = []

        for day in days:
            transactions = Transaction.objects.filter(
                position__project=project,
                investment_date__date=day
            )
            total_fund = transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "date": day.isoformat(),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)


class ProjectFundStatisticsLast90DaysView(APIView):

    @swagger_auto_schema(
        operation_description="Get total fund for a specific project for the last 90 days.",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last 90 days",
                examples={
                    'application/json': [
                        {"date": "2024-01-02", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        days = [(today - timedelta(days=i)) for i in range(90)]

        result = []

        for day in days:
            transactions = Transaction.objects.filter(
                position__project=project,
                investment_date__date=day
            )
            total_fund = transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "date": day.isoformat(),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)


class ProjectFundStatisticsLastYearView(APIView):

    @swagger_auto_schema(
        operation_description="Get total fund for a specific project for the last year (monthly).",
        responses={
            200: openapi.Response(
                description="A list of fund statistics for the last year",
                examples={
                    'application/json': [
                        {"month": "2024-01", "fund": "12313"},
                        # ... more examples ...
                    ]
                }
            )
        }
    )
    def get(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)

        today = timezone.now().date()
        months = [(today.replace(day=1) - timedelta(days=i*30)).replace(day=1) for i in range(12)]

        result = []

        for month in months:
            transactions = Transaction.objects.filter(
                position__project=project,
                investment_date__year=month.year,
                investment_date__month=month.month
            )
            total_fund = transactions.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0

            result.append({
                "month": month.strftime("%Y-%m"),
                "fund": f"{total_fund:.0f}"
            })

        return Response(result)