from django.contrib import admin
from expenses.models import (
    Profile, Group, GroupMembership, Expense, ExpenseSplit,
    Settlement, ImportReport, Category, Import, Anomaly
)

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Expense)
admin.site.register(ExpenseSplit)
admin.site.register(Settlement)
admin.site.register(Category)
admin.site.register(Import)
admin.site.register(Anomaly)
admin.site.register(ImportReport)

