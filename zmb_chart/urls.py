"""
URL configuration for zmb_chart project.

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
from django.urls import path, include, re_path
from chart.views import (
    hotwater,
    mashlauter,
    wortkettle,
    icewater,
    glycol,
    fv,
    fv1_2,
    fv3_4,
    fv5_6,
    fv7_8,
    fv9_10,
    fv11_12,
    fv13_14,
    fv15_16,
    fv17_18,
    fv19_20,
    fv21_22,
    DefaultFormByFieldView,
    DefaultFormsetView,
    DefaultFormView,
    FormHorizontalView,
    FormInlineView,
    FormWithFilesView,
    HomePageView,
    MiscView,
    PaginationView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hotwater, name="hotwater"),
    re_path(r"^hotwater$", hotwater, name="hotwater"),
    re_path(r"^mashlauter$", mashlauter, name="mashlauter"),
    re_path(r"^wortkettle$", wortkettle, name="wortkettle"),
    re_path(r"^icewater$", icewater, name="icewater"),
    re_path(r"^glycol$", glycol, name="glycol"),
    re_path(r"^fv$", fv, name="fv"),
    re_path(r"^fv1_2$", fv1_2, name="fv1_2"),
    re_path(r"^fv3_4$", fv3_4, name="fv3_4"),
    re_path(r"^fv5_6$", fv5_6, name="fv5_6"),
    re_path(r"^fv7_8$", fv7_8, name="fv7_8"),
    re_path(r"^fv9_10$", fv9_10, name="fv9_10"),
    re_path(r"^fv11_12$", fv11_12, name="fv11_12"),
    re_path(r"^fv13_14$", fv13_14, name="fv13_14"),
    re_path(r"^fv15_16$", fv15_16, name="fv15_16"),
    re_path(r"^fv17_18$", fv17_18, name="fv17_18"),
    re_path(r"^fv19_20$", fv19_20, name="fv19_20"),
    re_path(r"^fv21_22$", fv21_22, name="fv21_22"),
    re_path(r"^home$", HomePageView.as_view(), name="home"),
    re_path(r"^formset$", DefaultFormsetView.as_view(), name="formset_default"),
    re_path(r"^form$", DefaultFormView.as_view(), name="form_default"),
    re_path(r"^form_by_field$", DefaultFormByFieldView.as_view(), name="form_by_field"),
    re_path(r"^form_horizontal$", FormHorizontalView.as_view(), name="form_horizontal"),
    re_path(r"^form_inline$", FormInlineView.as_view(), name="form_inline"),
    re_path(r"^form_with_files$", FormWithFilesView.as_view(), name="form_with_files"),
    re_path(r"^pagination$", PaginationView.as_view(), name="pagination"),
    re_path(r"^misc$", MiscView.as_view(), name="misc"),
]
