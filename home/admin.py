from django.contrib import admin
from .models import RequestBlood, BloodGroup, Donor  # Import all models you need

# Register other models
admin.site.register(BloodGroup)
admin.site.register(Donor)

# Register RequestBlood with a custom admin class
@admin.register(RequestBlood)
class RequestBloodAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'blood_group', 'date', 'city', 'address', 'is_fulfilled')
    list_filter = ('is_fulfilled',)
    search_fields = ('name', 'phone', 'city')


