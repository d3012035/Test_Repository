from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from Edrive.views import PortfolioView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Edrive/', include('Edrive.urls')),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('', PortfolioView.as_view(), name='root_portfolio'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
