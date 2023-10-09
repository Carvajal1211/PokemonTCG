from django.contrib import admin
from django.urls import path, include
import core.views as core_views
import core.api as core_apis
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL's
    path('admin/', admin.site.urls),
    path('pokemon_tcg/', core_views.Pokemon_tcg, name="pokemon_tcg"),
    path('pokemon_battle/', core_views.Pokemon_battle, name="pokemon_battle"),
    path('pokemon/', core_views.Pokemon, name="pokemon"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
