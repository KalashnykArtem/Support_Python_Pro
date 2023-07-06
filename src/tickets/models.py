from django.conf import settings
from django.db import models

from tickets.constants import TicketStatus


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    visibility = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField(default=TicketStatus.NOT_STARTED)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="user_tickets",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="manager_tickets",
        null=True,
    )

    class Meta:
        db_table = "tickets"


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="messages",  # noqa: E501
    )
    request = models.ForeignKey(
        "tickets.Ticket", on_delete=models.RESTRICT, related_name="messages"
    )

    class Meta:
        db_table = "messages"
