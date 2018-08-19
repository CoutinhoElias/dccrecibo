from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, ReceiptMovimento, Receipt


class ReceiptMovimentoInline(admin.TabularInline):
    model = ReceiptMovimento
    extra = 1

class ReceiptModelAdmin(admin.ModelAdmin):
    readonly_fields = ['value_total']
    inlines = [ReceiptMovimentoInline]
    list_display = ['person', 'value_total', 'vehicle', 'chassis', 'color']

    def value_total(self, obj):
        if not obj.value_total:
            return obj.value_total
        else:
            return '%.2f' % obj.value_total


admin.site.register(Person)
admin.site.register(Receipt, ReceiptModelAdmin)