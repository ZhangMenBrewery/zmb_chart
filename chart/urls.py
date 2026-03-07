from django.urls import path

from . import views
from . import api_views

urlpatterns = [
    path("", views.index, name="index"),
    # API endpoints for chart data
    path('api/hotwater/', api_views.hotwater_api, name='hotwater_api'),
    path('api/mashlauter/', api_views.mashlauter_api, name='mashlauter_api'),
    path('api/wortkettle/', api_views.wortkettle_api, name='wortkettle_api'),
    path('api/icewater/', api_views.icewater_api, name='icewater_api'),
    path('api/glycol/', api_views.glycol_api, name='glycol_api'),
    path('api/fv/', api_views.fv_api, name='fv_api'),
    path('api/fv-list/', api_views.fv_list_api, name='fv_list_api'),
]