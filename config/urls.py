
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI view (visual interactive documentation)
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc view (alternative visual documentation layout)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]