from orders.models import Order
from django.db.models import Count


# This function display in the dasboard how many items are in the basket
def basket_item_count(request):

    # Guard clause
    if not request.user.is_authenticated:
        return {"basket_count": 0}

    # Unpaid orders = active basket
    get_count = Order.objects.filter(paid_at__isnull=True)
        
    if request.user.profile.role != "admin":
        get_count = get_count.filter(user = request.user)
        
    # Count jobs (items) inside the basket
    count = get_count.aggregate(
        total=Count("transactions")
    )["total"] or 0

    return {
        "basket_count": count
    }
