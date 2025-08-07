from django.contrib import admin
from .models import (
    Account, MState, MAddress, MCompany,
    MDepartment, MGrade, MEmployee, MPaygrade,
    MPay, TLeave, TAchievement
)

# Register all models to make them accessible in the admin panel
admin.site.register(Account)
admin.site.register(MState)
admin.site.register(MAddress)
admin.site.register(MCompany)
admin.site.register(MDepartment)
admin.site.register(MGrade)
admin.site.register(MEmployee)
admin.site.register(MPaygrade)
admin.site.register(MPay)
admin.site.register(TLeave)
admin.site.register(TAchievement)
