from django.db import models


class DesignTypeChoices(models.TextChoices):
    ICON = 'icon', 'Icon'
    LOGO = 'logo', 'Logo'
    POSTER = 'poster', 'Poster'
