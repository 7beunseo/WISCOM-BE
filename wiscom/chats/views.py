from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponseRedirect

class ChatView(APIView):
    def get(self, request, *args, **kwargs):
        access_token = settings.KAKAO_API_ACCESS_TOKEN
        chat_room_id = settings.KAKAO_CHAT_ROOM_ID

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        url = f'http://pf.kakao.com/{chat_room_id}/chat'

        return HttpResponseRedirect(url)
