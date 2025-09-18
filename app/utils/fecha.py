# app/utils/fechas.py
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

def formatear_fecha_esp(dt):
    if dt is None:
        return ""
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        dt_madrid = dt.astimezone(ZoneInfo("Europe/Madrid"))
        print("hora en Madrid:", dt_madrid)
        return dt_madrid.strftime('%d/%m/%Y %H:%M')
    except Exception as e:
        return str(dt)