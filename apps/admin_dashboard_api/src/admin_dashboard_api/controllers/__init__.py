"""HTTP controllers."""

from admin_dashboard_api.controllers.auth_controller import router as auth_router
from admin_dashboard_api.controllers.health_controller import router as health_router

__all__ = ("auth_router", "health_router")
