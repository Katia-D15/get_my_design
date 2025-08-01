def automatic_price(order):
    """
    Calculate and return the automatic price
    for an order based on design type and size.
    """
    price = 0

    if order.design_type == 'icon':
        price += 15.55
    elif order.design_type == 'logo':
        price += 25.55
    elif order.design_type == 'poster':
        price += 35.55

    if order.size == 'small':
        price += 5
    elif order.size == 'medium':
        price += 10
    elif order.size == 'large':
        price += 20

    return price
