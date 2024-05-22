from django.db import models


class MessageContent(models.Model):
    hash = models.CharField(max_length=200)
    message_text = models.CharField(max_length=1000)


class MessageInfo(models.Model):
    message = models.ForeignKey(MessageContent, on_delete=models.CASCADE)
    from_name = models.CharField(max_length=30)
    to_name = models.CharField(max_length=30)
    timestamp = models.IntegerField()
