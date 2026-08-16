from django.contrib import admin
from .models import CoffeeOrder, CoffeeVariety, Store, coffeeCertificate, coffeeReview

# Register your models here.
class coffeeReviewInline(admin.TabularInline):
    model = coffeeReview
    extra=2

class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ('name','type','date_added')
    inlines=[coffeeReviewInline]

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name','location')
    filter_horizontal = ('coffee_varieties', 'staff_members')

class coffeeCertificateAdmin(admin.ModelAdmin):
    list_display= ('coffee','certificate_number')

class CoffeeOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'coffee_variety', 'quantity', 'store', 'user', 'status', 'created_at')
    list_filter = ('status', 'store', 'coffee_variety')
    search_fields = ('user__username', 'store__name', 'coffee_variety__name')
    list_editable = ('status',)


admin.site.register(CoffeeVariety, ChaiVarietyAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(coffeeCertificate, coffeeCertificateAdmin)
admin.site.register(CoffeeOrder, CoffeeOrderAdmin)
