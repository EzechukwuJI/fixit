def is_tradesman(user):
	return user.groups.filter(name = 'Tradesmen').exists()


