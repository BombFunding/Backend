from django.db.models import Count, Q
from project.models import Project, CATEGORIES
from categories.models import LikedSubcategories
from .serializers import ProjectListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from position.utils import has_open_position

# Common parameters for Swagger documentation
category_param = openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING)
subcategory_param = openapi.Parameter('subcategory', openapi.IN_QUERY, type=openapi.TYPE_STRING)
my_favorite_param = openapi.Parameter('my_favorite', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
search_param = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING)
results_per_page_param = openapi.Parameter('results_per_page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
page_number_param = openapi.Parameter('page_number', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

def filter_projects(request, queryset):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    my_favorite = request.GET.get('my_favorite') == 'true'
    search_query = request.GET.get('search')
    
    if category:
        if category in CATEGORIES:
            category_subcategories = CATEGORIES[category]
            combined_queryset = Project.objects.none()
            for category_subcategory in category_subcategories:
                combined_queryset |= queryset.filter(subcategories__contains=[category_subcategory])
            queryset = combined_queryset
    
    if subcategory:
        queryset = queryset.filter(subcategories__contains=[subcategory])
    
    if my_favorite and request.user.is_authenticated:
        try:
            liked_subcategories = LikedSubcategories.objects.get(user=request.user)
            combined_queryset = Project.objects.none()
            for subcategory in liked_subcategories.subcategories:
                combined_queryset |= queryset.filter(subcategories__contains=[subcategory])
            queryset = combined_queryset
        except LikedSubcategories.DoesNotExist:
            queryset = queryset.none()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    queryset = queryset.filter(id__in=[project.id for project in queryset if has_open_position(project)])
    
    return queryset

def get_total_pages(queryset, results_per_page):
    total_items = queryset.count()
    total_pages = (total_items + results_per_page - 1) // results_per_page
    return total_pages

def paginate_queryset(queryset, request):
    results_per_page = int(request.GET.get('results_per_page', 10))
    page_number = int(request.GET.get('page_number', 1))
    
    start_idx = (page_number - 1) * results_per_page
    end_idx = start_idx + results_per_page
    
    return queryset[start_idx:end_idx], get_total_pages(queryset, results_per_page)

@swagger_auto_schema(
    method='get',
    manual_parameters=[category_param, subcategory_param, my_favorite_param, 
                      search_param, results_per_page_param, page_number_param]
)
@api_view(['GET'])
def top_visited_projects(request):
    queryset = Project.objects.annotate(
        total_visits=Count('statistics__views')
    ).order_by('-total_visits')
    
    queryset = filter_projects(request, queryset)
    paginated_queryset, total_pages = paginate_queryset(queryset, request)
    
    serializer = ProjectListSerializer(paginated_queryset, many=True, context={'request': request})
    return Response({
        'result_count': queryset.count(),
        'total_pages': total_pages,
        'results': serializer.data
    })

@swagger_auto_schema(
    method='get',
    manual_parameters=[category_param, subcategory_param, my_favorite_param, 
                      search_param, results_per_page_param, page_number_param]
)
@api_view(['GET'])
def top_liked_projects(request):
    queryset = Project.objects.annotate(
        total_likes=Count('statistics__likes')
    ).order_by('-total_likes')
    
    queryset = filter_projects(request, queryset)
    paginated_queryset, total_pages = paginate_queryset(queryset, request)
    
    serializer = ProjectListSerializer(paginated_queryset, many=True, context={'request': request})
    return Response({
        'result_count': queryset.count(),
        'total_pages': total_pages,
        'results': serializer.data
    })

@swagger_auto_schema(
    method='get',
    manual_parameters=[category_param, subcategory_param, my_favorite_param, 
                      search_param, results_per_page_param, page_number_param]
)
@api_view(['GET'])
def most_recent_projects(request):
    queryset = Project.objects.all().order_by('-creation_date')
    
    queryset = filter_projects(request, queryset)
    paginated_queryset, total_pages = paginate_queryset(queryset, request)
    
    serializer = ProjectListSerializer(paginated_queryset, many=True, context={'request': request})
    return Response({
        'result_count': queryset.count(),
        'total_pages': total_pages,
        'results': serializer.data
    })
