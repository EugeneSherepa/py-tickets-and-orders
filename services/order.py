from typing import Optional

from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, User, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None) -> Order:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
