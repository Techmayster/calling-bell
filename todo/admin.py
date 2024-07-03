

from django.contrib import admin
from .models import User_information,data_logging,Remote_information


@admin.register(User_information,data_logging,Remote_information)
class PersonAdmin(admin.ModelAdmin):
    pass