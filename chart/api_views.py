# chart/api_views.py
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from .models import (
    PlcHotwater, PlcMashlauter, PlcWortkettle, PlcIcewater,
    PlcGlycol1, PlcGlycol2,
    PlcFv1, PlcFv2, PlcFv3, PlcFv4, PlcFv5, PlcFv6,
    PlcFv7, PlcFv8, PlcFv9, PlcFv10, PlcFv11, PlcFv12,
    PlcFv13, PlcFv14, PlcFv15, PlcFv16, PlcFv17, PlcFv18,
    PlcFv19, PlcFv20, PlcFv21, PlcFv22
)
from datetime import datetime, timedelta, timezone as tz
import pytz


def get_data_range(request):
    """獲取數據時間範圍參數"""
    days = int(request.GET.get('days', 30))
    # 資料庫中的時間是台灣時間（naive datetime），Django 設定 USE_TZ=False 不會進行時區轉換
    # 使用 pytz 的 Asia/Taipei 來獲取正確的台灣時間
    taipei_tz = pytz.timezone('Asia/Taipei')
    # 獲取當前台灣時間
    now_taipei = timezone.now().astimezone(taipei_tz)
    # 資料庫中的時間是台灣時間（naive datetime），Django 設定 USE_TZ=False 不會進行時區轉換
    start_time = (now_taipei - timedelta(days=days)).replace(tzinfo=None)
    end_time = now_taipei.replace(tzinfo=None)
    return start_time, end_time


def hotwater_api(request):
    """熱水罐 API - 返回 JSON 數據"""
    days = int(request.GET.get('days', 30))
    cache_key = f'api_hotwater_data_{days}d'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        queryset = PlcHotwater.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).order_by('timestamp').values(
            'timestamp', 'temperature', 'setpoint', 'valve', 'volume', 'pump'
        )
        
        # 處理時區：Django 設定 USE_TZ=False 不會進行時區轉換
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        data = {
            'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
            'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
            'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
            'valve': [float(item['valve']) if item['valve'] else 0 for item in queryset],
            'volume': [float(item['volume']) if item['volume'] else 0 for item in queryset],
            'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
        }
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def mashlauter_api(request):
    """糖化鍋 API - 返回 JSON 數據"""
    days = int(request.GET.get('days', 30))
    cache_key = f'api_mashlauter_data_{days}d'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        queryset = PlcMashlauter.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).order_by('timestamp').values(
            'timestamp', 'temperature', 'setpoint', 'valve', 'pump',
            'pumpspeed', 'agitator', 'agitatorspeed', 'flowmeter'
        )
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        data = {
            'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
            'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
            'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
            'valve': [float(item['valve']) if item['valve'] else 0 for item in queryset],
            'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
            'pumpspeed': [float(item['pumpspeed']) if item['pumpspeed'] else 0 for item in queryset],
            'agitator': [float(item['agitator']) if item['agitator'] else 0 for item in queryset],
            'agitatorspeed': [float(item['agitatorspeed']) if item['agitatorspeed'] else 0 for item in queryset],
            'flowmeter': [float(item['flowmeter']) if item['flowmeter'] else 0 for item in queryset],
        }
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def wortkettle_api(request):
    """煮沸鍋 API - 返回 JSON 數據"""
    days = int(request.GET.get('days', 30))
    cache_key = f'api_wortkettle_data_{days}d'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        queryset = PlcWortkettle.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).order_by('timestamp').values(
            'timestamp', 'temperature', 'setpoint', 'valve1', 'valve2',
            'chimneytemperature', 'pump', 'pumpspeed', 'flowmeter', 'flowvolume'
        )
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        data = {
            'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
            'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
            'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
            'valve1': [float(item['valve1']) if item['valve1'] else 0 for item in queryset],
            'valve2': [float(item['valve2']) if item['valve2'] else 0 for item in queryset],
            'chimneytemperature': [float(item['chimneytemperature']) if item['chimneytemperature'] else 0 for item in queryset],
            'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
            'pumpspeed': [float(item['pumpspeed']) if item['pumpspeed'] else 0 for item in queryset],
            'flowmeter': [float(item['flowmeter']) if item['flowmeter'] else 0 for item in queryset],
            'flowvolume': [float(item['flowvolume']) if item['flowvolume'] else 0 for item in queryset],
        }
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def icewater_api(request):
    """冰水罐 API - 返回 JSON 數據"""
    days = int(request.GET.get('days', 30))
    cache_key = f'api_icewater_data_{days}d'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        queryset = PlcIcewater.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).order_by('timestamp').values(
            'timestamp', 'volume', 'pump'
        )
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        data = {
            'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
            'volume': [float(item['volume']) if item['volume'] else 0 for item in queryset],
            'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
        }
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def glycol_api(request):
    """冷媒罐 API - 返回 JSON 數據"""
    tank = request.GET.get('tank', '1')
    days = int(request.GET.get('days', 30))
    
    if tank == '1':
        cache_key = f'api_glycol1_data_{days}d'
        ModelClass = PlcGlycol1
    else:
        cache_key = f'api_glycol2_data_{days}d'
        ModelClass = PlcGlycol2
    
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        # 根據冷媒罐編號選擇正確的字段
        if tank == '1':
            queryset = ModelClass.objects.filter(
                timestamp__gte=start_time,
                timestamp__lte=end_time
            ).order_by('timestamp').values(
                'timestamp', 'temperature', 'setpoint', 'cooler1', 'cooler2', 'pump'
            )
        else:
            queryset = ModelClass.objects.filter(
                timestamp__gte=start_time,
                timestamp__lte=end_time
            ).order_by('timestamp').values(
                'timestamp', 'temperature', 'setpoint', 'cooler1', 'cooler2', 'pump'
            )
        
        # 處理 cooler1/cooler2 字段
        if tank == '1':
            data = {
                'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
                'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
                'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
                'cooler1': [float(item['cooler1']) if item['cooler1'] else 0 for item in queryset],
                'cooler2': [float(item['cooler2']) if item['cooler2'] else 0 for item in queryset],
                'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
            }
        else:
            data = {
                'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
                'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
                'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
                'cooler1': [float(item['cooler1']) if item['cooler1'] else 0 for item in queryset],
                'cooler2': [float(item['cooler2']) if item['cooler2'] else 0 for item in queryset],
                'pump': [float(item['pump']) if item['pump'] else 0 for item in queryset],
            }
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def fv_api(request):
    """發酵罐 API - 返回 JSON 數據"""
    fv_number = request.GET.get('fv', '1')
    days = int(request.GET.get('days', 30))
    
    try:
        fv_num = int(fv_number)
    except ValueError:
        return JsonResponse({'error': 'Invalid FV number'}, status=400)
    
    # 獲取對應的模型類
    model_map = {
        1: PlcFv1, 2: PlcFv2, 3: PlcFv3, 4: PlcFv4,
        5: PlcFv5, 6: PlcFv6, 7: PlcFv7, 8: PlcFv8,
        9: PlcFv9, 10: PlcFv10, 11: PlcFv11, 12: PlcFv12,
        13: PlcFv13, 14: PlcFv14, 15: PlcFv15, 16: PlcFv16,
        17: PlcFv17, 18: PlcFv18, 19: PlcFv19, 20: PlcFv20,
        21: PlcFv21, 22: PlcFv22
    }
    
    ModelClass = model_map.get(fv_num)
    if not ModelClass:
        return JsonResponse({'error': 'FV not found'}, status=404)
    
    cache_key = f'api_fv{fv_num}_data_{days}d'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        # FV17 以上有額外字段
        if fv_num >= 17:
            queryset = ModelClass.objects.filter(
                timestamp__gte=start_time,
                timestamp__lte=end_time
            ).order_by('timestamp').values(
                'timestamp', 'temperature', 'setpoint', 'valve1', 'valve2',
                'psi', 'psi_sp', 'co2vol', 'co2vol_sp', 'valve3'
            )
            
            data = {
                'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
                'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
                'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
                'valve1': [float(item['valve1']) if item['valve1'] else 0 for item in queryset],
                'valve2': [float(item['valve2']) if item['valve2'] else 0 for item in queryset],
                'psi': [float(item['psi']) if item['psi'] else 0 for item in queryset],
                'psi_sp': [float(item['psi_sp']) if item['psi_sp'] else 0 for item in queryset],
                'co2vol': [float(item['co2vol']) if item['co2vol'] else 0 for item in queryset],
                'co2vol_sp': [float(item['co2vol_sp']) if item['co2vol_sp'] else 0 for item in queryset],
                'valve3': [float(item['valve3']) if item['valve3'] else 0 for item in queryset],
            }
        else:
            queryset = ModelClass.objects.filter(
                timestamp__gte=start_time,
                timestamp__lte=end_time
            ).order_by('timestamp').values(
                'timestamp', 'temperature', 'setpoint', 'valve1', 'valve2'
            )
            
            data = {
                'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
                'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
                'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
                'valve1': [float(item['valve1']) if item['valve1'] else 0 for item in queryset],
                'valve2': [float(item['valve2']) if item['valve2'] else 0 for item in queryset],
            }
        
        cache.set(cache_key, data, timeout=300)  # 5 分鐘緩存
    else:
        data = cached_data
    
    return JsonResponse(data)


def fv_list_api(request):
    """獲取所有發酵罐數據列表"""
    fv_numbers = request.GET.getlist('fv[]') or request.GET.get('fvs', '1-22').split('-')
    
    result = {}
    cache_key = 'api_fv_list'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        start_time, end_time = get_data_range(request)
        
        def format_timestamp(ts):
            if ts is None:
                return None
            return ts.isoformat()
        
        for fv_num in range(1, 23):
            ModelClass = globals()[f'PlcFv{fv_num}']
            
            queryset = ModelClass.objects.filter(
                timestamp__gte=start_time,
                timestamp__lte=end_time
            ).order_by('timestamp').values(
                'timestamp', 'temperature', 'setpoint', 'valve1', 'valve2'
            )
            
            data = {
                'timestamps': [format_timestamp(item['timestamp']) for item in queryset],
                'temperature': [float(item['temperature']) if item['temperature'] else 0 for item in queryset],
                'setpoint': [float(item['setpoint']) if item['setpoint'] else 0 for item in queryset],
                'valve1': [float(item['valve1']) if item['valve1'] else 0 for item in queryset],
                'valve2': [float(item['valve2']) if item['valve2'] else 0 for item in queryset],
            }
            
            result[f'FV{fv_num}'] = data
        
        cache.set(cache_key, result, timeout=300)  # 5 分鐘緩存
    else:
        result = cached_data
    
    return JsonResponse(result)
