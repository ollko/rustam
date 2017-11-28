from .cart import Cart


def cart(request):
	a=Cart(request)
	return {'cart': Cart(request)}