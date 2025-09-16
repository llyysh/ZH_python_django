"""acrn_issues_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class_based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('table_example', views.table_show),    
    re_path(r'^news_search$', views.news_search),
    re_path(r'^news_filter$', views.news_filter),
    re_path(r'^download_excel', views.download_excel),

    path('tables/', views.list_tables, name="list_tables"),
    path('tables/<str:table_name>/', views.show_table, name="show_table"),
]

###################################################################################################

# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.index, name="index"),   # 首页，显示所有表
#     path("table/<str:table_name>/", views.table_detail, name="table_detail"),
#     path("download/<str:table_name>/", views.download_csv, name="download_csv"),
# ]
