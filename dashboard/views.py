from django.shortcuts import render
from django.http import JsonResponse
from geoip2 import database
from dashboard.models import SnortDetails
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@require_http_methods(["GET"])
def home(request):
    if request.method == "GET":
        return render(request, "dashboard/home.html")


@csrf_exempt
@require_http_methods(["POST"])
def attack_data(request):
    attack_details = SnortDetails.objects.values()[:1000]
    final_data = []
    for data in attack_details:
        src_data, dst_data, timestamp = get_ip_details(data)
        if src_data and dst_data and timestamp:
            final_data.append({**src_data, **dst_data, **timestamp})

    return JsonResponse({"status": 200, "data": final_data})


@csrf_exempt
@require_http_methods(["POST"])
def get_attacking_countries(request):
    try:
        top_countries = SnortDetails.objects.exclude(src_country__isnull=True).exclude(src_country="").values("src_country").annotate(
            count=Count
            ("src_country")).order_by("-count")[:10]
        top_countries = [top_country["src_country"] for top_country in top_countries]
        status_code = 200
    except Exception as e:
        print(e)
        status_code = 404
        top_countries = None
    return JsonResponse({"status": status_code, "countries": top_countries})


@csrf_exempt
@require_http_methods(["POST"])
def get_top_attacks(request):
    try:
        top_attacks = SnortDetails.objects.exclude(msg__isnull=True).values("msg").annotate(
            count=Count("msg")).order_by("-count")[:10]
        top_attacks = [top_attack["msg"] for top_attack in top_attacks]
        status_code = 200
    except Exception as e:
        status_code = 404
        top_attacks = None
    return JsonResponse({"status": status_code, "attacks": top_attacks})


def get_ip_details(attack_details):
    geo_database = database.Reader("/home/blackout/Projects/sql/GeoLite2-City.mmdb")
    src_ip = attack_details["src"]
    dst_ip = attack_details["dst"]
    rest_data = {"timestamp": "11 Jul 2020 00:08:20AM", "rule": attack_details["msg"]}
    try:
        src_details = geo_database.city(src_ip)
        dst_details = geo_database.city(dst_ip)
        src_city_name = src_details.city.name
        dst_city_name = dst_details.city.name
        src_data = {
            "latitude": src_details.location.latitude,
            "longitude": src_details.location.longitude,
            "countrycode": src_details.country.iso_code,
            "source_ip": src_ip,
            "source_port": attack_details["srcport"],
            "country": src_details.country.name,
            "city": src_city_name if src_city_name else ""
        }
        dst_data = {
            "latitude2": dst_details.location.latitude,
            "longitude2": dst_details.location.longitude,
            "countrycode2": dst_details.country.iso_code,
            "dest_ip": dst_ip,
            "dst_port": attack_details["dstport"],
            "country2": dst_details.country.name,
            "city2": dst_city_name if dst_city_name else ""
        }
    except:
        return {}, {}, {}

    return src_data, dst_data, rest_data
