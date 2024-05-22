from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Max
from .models import MessageContent, MessageInfo
import json


@csrf_exempt
def test(request):
    if request.method == "POST":
        try:
            print(request.body)
            print(type(request.body))
            data = json.loads(request.body)
            return JsonResponse({"data": "Success"})
        except:
            return JsonResponse({"data": "Fail"})


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            timestamp = data["timestamp"]
            from_name = data["from"]
            to_name = data["to"]
            hash_data = data["hash"]
            message = data["message"]
            new_content = MessageContent(hash=hash_data, message_text=message)
            new_content.save()
            new_info = MessageInfo(from_name=from_name, to_name=to_name, timestamp=timestamp, message=new_content)
            new_info.save()
            return JsonResponse({"status": "good"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"status": "parse error"})
    else:
        return JsonResponse({"status": "wrong method"})


def get_message(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            from_name = data["from"]
            to_name = data["to"]
            max_value_data = MessageInfo.objects.filter(from_name=from_name, to_name=to_name).aggregate(Max("timestamp"))
            max_value = max_value_data["timestamp__max"]
            if max_value is None:
                return JsonResponse({"status": "name error"})
            info_entity = MessageInfo.objects.filter(timestamp=max_value)[0]
            content_entity = MessageContent.objects.filter(pk=info_entity.message.pk)[0]
            return JsonResponse({
                "hash": content_entity.hash,
                "message": content_entity.message_text
            })
        except Exception as ex:
            return JsonResponse({"status": "parse error"})
    else:
        return JsonResponse({"status": "wrong method"})
