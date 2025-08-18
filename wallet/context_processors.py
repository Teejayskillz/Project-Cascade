# wallet/context_processors.py
from .models import Wallet

def wallet_balance(request):
    """
    Provides the user's wallet information to all templates.
    """
    if request.user.is_authenticated:
        try:
            user_wallet = request.user.wallet
            return {
                'user_wallet': user_wallet,
                'wallet_balance': user_wallet.balance
            }
        except Wallet.DoesNotExist:
            return {
                'user_wallet': None,
                'wallet_balance': 0
            }
    
    return {
        'user_wallet': None,
        'wallet_balance': None
    }