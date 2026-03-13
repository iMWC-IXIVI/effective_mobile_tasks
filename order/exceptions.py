class UserException(Exception): pass
class OrderException(Exception): pass
class DiscountException(Exception): pass
class UserValueError(UserException): pass
class OrderValueError(OrderException): pass
class DiscountValueError(DiscountException): pass
