from django.urls import path
from dashboard.views import home, attack_data, get_top_attacks, get_attacking_countries


urlpatterns = [
    path("", home, name="home"),
    path("attack_data", attack_data),
    path("get_top_attacks", get_top_attacks),
    path("get_attacking_countries", get_attacking_countries)
]