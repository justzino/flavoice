from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Voice(TimeStampedModel):

    """ File Model """

    file = models.FileField(upload_to="voices", blank=False, null=False)
    description = models.CharField(max_length=255)
