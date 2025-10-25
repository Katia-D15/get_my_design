from django.urls import path
from . import views

urlpatterns = [

    path("create-order/", views.create_order, name="create_order"),
    path(
        "review/<str:order_number>/",
        views.review_order,
        name="review_order"),
    path("", views.my_orders, name="my_orders"),
    path("previous/", views.previous_work, name="previous_work"),
    path(
        "submit-comment/<int:order_id>/",
        views.submit_comment,
        name="submit_comment"),
    path(
        "edit_comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment"
        ),
    path(
        "delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"
    )

]
