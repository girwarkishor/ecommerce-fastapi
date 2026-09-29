from app.core.database import Base
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole

__all__ = ["Base", "Order", "OrderItem", "OrderStatus", "Product", "User", "UserRole"]

# This is a special Python variable.
# It explicitly tells Python: "When someone types from app.models import *, these are the only things they are allowed to see."
# It keeps the package clean by hiding internal helper variables or temporary imports.
