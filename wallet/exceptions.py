class WalletExceptions(Exception): pass
class WalletLTZero(WalletExceptions): pass
class ValueReplenishmentLTZero(WalletExceptions): pass
class WalletDoesNotFound(WalletExceptions): pass