from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .models import *
from datetime import datetime, timedelta

import pandas as pd

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go

from .forms import ContactForm, ContactFormSet, FilesForm

# Create your views here.

def hotwater(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"

    cached_data = cache.get('hotwater_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcHotwater.objects.only('timestamp', 'temperature', 'setpoint', 'valve', 'volume', 'pump').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('hotwater_data', df, timeout=300)

    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="加熱",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve"], fill_value=0)))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="蒸氣閥",mode="lines", x=df["timestamp"], y=df["valve"].multiply(1, fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="體積",mode="lines", x=df["timestamp"], y=df["volume"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="熱水泵",mode="lines", x=df["timestamp"], y=df["pump"].multiply(1, fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    
    fig.layout.on_change(
        lambda obj, xrange, yrange: print("%s-%s" % (xrange, yrange)),
        ('xaxis', 'range'), ('yaxis', 'range'))
    plots['HotWater'] = plot(fig ,output_type='div')     
    return render(request, 'chart/hotwater.html', context=plots)

def mashlauter(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('mashlauter_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcMashlauter.objects.only('timestamp', 'temperature', 'setpoint', 'valve', 'pump', 'pumpspeed', 'agitator', 'agitatorspeed', 'flowmeter').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('mashlauter_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="加熱",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve"].astype(int), fill_value=0)))
    fig.add_trace(go.Scatter(name="糖化泵",mode="lines", x=df["timestamp"], y=df["pumpspeed"].multiply(df["pump"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="攪拌",mode="lines", x=df["timestamp"], y=df["agitatorspeed"].multiply(df["agitator"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="流量",mode="lines", x=df["timestamp"], y=df["flowmeter"], visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['MashLauter'] = plot(fig ,output_type='div')    
    return render(request, 'chart/mashlauter.html', context=plots)

def wortkettle(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('wortkettle_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcWortkettle.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'chimneytemperature' , 'pump', 'pumpspeed', 'flowmeter', 'flowvolume').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('wortkettle_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="上部加熱",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0)))
    fig.add_trace(go.Scatter(name="下部加熱",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0)))
    fig.add_trace(go.Scatter(name="麥汁泵",mode="lines", x=df["timestamp"], y=df["pumpspeed"].multiply(df["pump"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="煙囪溫度",mode="lines", x=df["timestamp"], y=df["chimneytemperature"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="流速",mode="lines", x=df["timestamp"], y=df["flowmeter"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="流量",mode="lines", x=df["timestamp"], y=df["flowvolume"], visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['WortKettle'] = plot(fig ,output_type='div')  
    return render(request, 'chart/wortkettle.html', context=plots)

def icewater(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('icewater_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcIcewater.objects.only('timestamp', 'volume', 'pump').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('icewater_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="體積",mode="lines", x=df["timestamp"], y=df["volume"]))
    fig.add_trace(go.Scatter(name="馬達",mode="lines", x=df["timestamp"], y=df["pump"].astype(int), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['IceWater'] = plot(fig ,output_type='div')  
    return render(request, 'chart/icewater.html', context=plots)

def glycol(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data1 = cache.get('glycol1_data')
    if cached_data1 is not None:
        df1 = cached_data1
    else:
        # 使用 only 加載特定字段
        queryset1 = PlcGlycol1.objects.only('timestamp', 'temperature', 'setpoint', 'cooler1', 'cooler2', 'pump').order_by('-timestamp').all()

        # 實現分頁
        paginator1 = Paginator(queryset1, 4000)
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)

        df1 = pd.DataFrame(list(page_obj1.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('glycol1_data', df1, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df1["timestamp"], y=df1["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df1["timestamp"], y=df1["setpoint"]))
    fig.add_trace(go.Scatter(name="製冷機#1",mode="lines", x=df1["timestamp"], y=df1["setpoint"].multiply(df1["cooler1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="製冷機#2",mode="lines", x=df1["timestamp"], y=df1["setpoint"].multiply(df1["cooler2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="馬達",mode="lines", x=df1["timestamp"], y=df1["pump"].astype(int), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['Glycol1'] = plot(fig ,output_type='div')

    cached_data2 = cache.get('glycol2_data')
    if cached_data2 is not None:
        df2 = cached_data2
    else:
        # 使用 only 加載特定字段
        queryset2 = PlcGlycol2.objects.only('timestamp', 'temperature', 'setpoint', 'cooler2', 'pump').order_by('-timestamp').all()

        # 實現分頁
        paginator2 = Paginator(queryset2, 4000)
        page_number2 = request.GET.get('page')
        page_obj2 = paginator2.get_page(page_number2)

        df2 = pd.DataFrame(list(page_obj2.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('glycol2_data', df2, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df2["timestamp"], y=df2["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df2["timestamp"], y=df2["setpoint"]))
    fig.add_trace(go.Scatter(name="製冷機",mode="lines", x=df2["timestamp"], y=df2["setpoint"].multiply(df2["cooler2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="馬達",mode="lines", x=df2["timestamp"], y=df2["pump"].astype(int), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['Glycol2'] = plot(fig ,output_type='div')  
    return render(request, 'chart/glycol.html', context=plots)

def fv(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    for i in range(1,23):
        cached_data = cache.get(f"FV{i}_data")
        if cached_data is not None:
            df = cached_data
        else:
            # 使用 only 加載特定字段
            if i>=17:
                queryset = eval(f"PlcFv{i}").objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()
            else:
                queryset = eval(f"PlcFv{i}").objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

            # 實現分頁
            paginator = Paginator(queryset, 4000)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            df = pd.DataFrame(list(page_obj.object_list.values()))
            
            # 將數據存儲到緩存中
            cache.set(f"FV{i}_data", df, timeout=300)

        fig = go.Figure()
        fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
        fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
        fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
        fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
        if i>=17:
            fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
            fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
            fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
            fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
            fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
        fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all")
                ])
            )
        )
        fig.update_yaxes(autorange = True, fixedrange= False)
        # def zoom(layout, x_range):
        #     in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
        #     fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]
        # fig.layout.on_change(zoom, 'xaxis.range')
        exec(f"plots['FV{i}'] = plot(fig ,output_type='div')")
    return render(request, 'chart/fv.html', context=plots)

def fv1_2(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"

    cached_data = cache.get('FV1_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv1.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV1_data', df, timeout=300)

    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV1'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV2_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv2.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV2_data', df, timeout=300)

    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV2'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv1_2.html', context=plots)

def fv3_4(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV3_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv3.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV3_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV3'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV4_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv4.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV4_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV4'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv3_4.html', context=plots)

def fv5_6(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV5_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv5.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV5_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV5'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV6_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv6.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV6_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV6'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv5_6.html', context=plots)

def fv7_8(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV7_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv7.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV7_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV7'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV8_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv8.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV8_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV8'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv7_8.html', context=plots)

def fv9_10(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV9_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv9.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV9_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV9'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV10_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv10.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV10_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV10'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv9_10.html', context=plots)

def fv11_12(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV11_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv11.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV11_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV11'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV12_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv12.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV12_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV12'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv11_12.html', context=plots)

def fv13_14(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV13_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv13.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV13_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV13'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV14_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv14.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV14_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV14'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv13_14.html', context=plots)

def fv15_16(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV15_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv15.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV15_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV15'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV16_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv16.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV16_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV16'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv15_16.html', context=plots)

def fv17_18(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV17_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv17.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV17_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV17'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV18_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv18.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV18_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV18'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv17_18.html', context=plots)

def fv19_20(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV19_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv19.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV19_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV19'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV20_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv20.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV20_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV20'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv19_20.html', context=plots)

def fv21_22(request):  
    plots = {}
    pd.options.plotting.backend = "plotly"
    cached_data = cache.get('FV21_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv21.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV21_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV21'] = plot(fig ,output_type='div')

    cached_data = cache.get('FV22_data')
    if cached_data is not None:
        df = cached_data
    else:
        # 使用 only 加載特定字段
        queryset = PlcFv22.objects.only('timestamp', 'temperature', 'setpoint', 'valve1', 'valve2', 'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3').order_by('-timestamp').all()

        # 實現分頁
        paginator = Paginator(queryset, 4000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        df = pd.DataFrame(list(page_obj.object_list.values()))
        
        # 將數據存儲到緩存中
        cache.set('FV22_data', df, timeout=300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="溫度",mode="lines", x=df["timestamp"], y=df["temperature"]))
    fig.add_trace(go.Scatter(name="設定溫度",mode="lines", x=df["timestamp"], y=df["setpoint"]))
    fig.add_trace(go.Scatter(name="上電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve1"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="下電磁閥",mode="lines", x=df["timestamp"], y=df["setpoint"].multiply(df["valve2"].astype(int), fill_value=0), visible="legendonly"))
    fig.add_trace(go.Scatter(name="壓力",mode="lines", x=df["timestamp"], y=df["psi"]))
    fig.add_trace(go.Scatter(name="設定壓力",mode="lines", x=df["timestamp"], y=df["psi_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="設定CO2體積",mode="lines", x=df["timestamp"], y=df["co2vol_sp"], visible="legendonly"))
    fig.add_trace(go.Scatter(name="洩壓閥",mode="lines", x=df["timestamp"], y=df["psi_sp"].multiply(df["valve3"].astype(int), fill_value=0), visible="legendonly"))
    fig.update_layout(xaxis_range=[datetime.today()-timedelta(days=1), datetime.today()])
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig.update_yaxes(autorange = True, fixedrange= False)
    plots['FV22'] = plot(fig ,output_type='div') 
    return render(request, 'chart/fv21_22.html', context=plots)


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class DefaultFormsetView(FormView):
    template_name = "app/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "app/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = "app/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "app/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "app/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "app/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "app/pagination.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append("Line %s" % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "app/misc.html"