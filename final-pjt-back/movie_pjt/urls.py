"""
URL configuration for movie_pjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # include 추가

# MEDIA_ROOT와 MEDIA_URL에 대한 url 지정에 필요한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', include('movies.urls')),  # movies앱 연결
    path('api/v1/accounts/', include('accounts.urls')),  # accounts앱 연결
    path('api/v1/accounts/', include('dj_rest_auth.urls')), # dj_rest_auth 라이브러리 연결
    path('api/v1/accounts/signup/', include('dj_rest_auth.registration.urls')), # signup 관련 연결
    path('api/v1/communities/', include('communities.urls')),  # communities앱 연결
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # settings.MEDIA_URL: 업로드 된 파일의 URL
    # settings.MEDIA_ROOT: 위 URL을 통해 참조하는 파일의 실제 위치
