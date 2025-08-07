from django.contrib.auth.backends import ModelBackend
from .models import Account

class AccountBackend(ModelBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        try:
            # Try to find a user with the provided user_id
            user = Account.objects.get(user_id=user_id)
            
            # Check if the provided password is correct
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            # No user was found, so authentication fails
            return None

    def get_user(self, pk):
        try:
            # This function is used by Django to retrieve the user object
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return None
