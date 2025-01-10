from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from app.api import router as app_router
from main.api import router as main_router

# Create a single NinjaAPI instance
api = NinjaAPI()

# Add routers for app and main
api.add_router("/app/", app_router, tags=["App API"])
api.add_router("/main/", main_router, tags=["Main API"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # All APIs are now under this instance
]
