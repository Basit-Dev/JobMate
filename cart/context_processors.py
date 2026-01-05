from .models import Transaction


# This function display in the dasboard how many items are in the basket
def basket_item_count(request):
    if request.user.is_authenticated and request.user.profile.role == "Admin":
        count = Transaction.objects.filter(
            status="open").count()
    elif request.user.is_authenticated and request.user.profile.role != "Admin":
        count = Transaction.objects.filter(
            user=request.user,
            status="open").count()
    else:
        count = 0

    return {
        "basket_count": count
    }
