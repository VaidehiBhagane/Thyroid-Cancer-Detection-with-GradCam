"""Routes package - modular API endpoints and functions"""
from api.routes.routes_endpoints import router
from api.routes.routes_functions import set_model

__all__ = ['router', 'set_model']
