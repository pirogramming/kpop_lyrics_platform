from uuid import uuid4
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        print(user)
        social_app_name = sociallogin.account.provider.upper()
        user_uuid = int(uuid4()) % 10000000000
        user.username = social_app_name + str(user_uuid)
        user.alias = user.username
        user.save()
        return user
