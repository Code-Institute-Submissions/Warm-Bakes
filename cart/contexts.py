def cart_contents(request):
    # make the content of the shopping cart available to all templates
    lesson_cart = request.session.get("lesson_shopping_cart",{})
    product_cart = request.session.get("product_shopping_cart",{})
    return {
        'lesson_shopping_cart':lesson_cart,
        'product_shopping_cart':product_cart,
        'number_of_items':int(len(product_cart)+len(lesson_cart))
    }