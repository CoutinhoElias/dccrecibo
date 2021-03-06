from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, ReceiptMovimento, Receipt, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'name')
    search_fields = ('id', 'name')


class ReceiptMovimentoInline(admin.TabularInline):
    model = ReceiptMovimento
    extra = 1


class ReceiptModelAdmin(admin.ModelAdmin):
    readonly_fields = ['value_total']
    inlines = [ReceiptMovimentoInline]
    list_display = ['person', 'value_total', 'vehicle', 'chassis', 'color']

    @staticmethod
    def value_total(obj):
        if not obj.value_total:
            return obj.value_total
        else:
            return '%.2f' % obj.value_total

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class PersonModelAdmin(admin.ModelAdmin):
    pass
    list_display = ('pk', 'name', 'cpf_cnpj')


admin.site.register(Person, PersonModelAdmin)
admin.site.register(Receipt, ReceiptModelAdmin)