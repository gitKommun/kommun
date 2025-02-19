
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('members/', include('members.urls')),  
    path('communities/', include('communities.urls')),  
    path('properties/', include('properties.urls')), 
    path('documents/', include('documents.urls')), 
    path('common_areas/', include('common_areas.urls')), 
    path('claims/', include('claims.urls')),
    path('finance/', include('finance.urls')),
    path('votes/', include('votes.urls')),
    path('core/', include('core.urls')),
    path('suppliers/', include('suppliers.urls')),
]
