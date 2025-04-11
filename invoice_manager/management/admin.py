from django.contrib import admin
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse


from django.contrib import admin

from management.models import Product, ProductRate, ProductInvoice, Invoice

import os

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")



@admin.action(description='Generate PDF')
def generate_pdf(modeladmin, request, queryset):
    for obj in queryset:
        # Render HTML with context data
        product_context = []
        id_counter = 0
        for invoice in obj.invoices.all():
            id_counter += 1
            product_name = invoice.product.product.name
            quantity = invoice.quantity
            price = invoice.price
            rate = invoice.product.rate
            product_context.append({"product_id": id_counter, "name": product_name, "quantity": quantity, "rate": rate, "price": price})

        html_string = render_to_string('invoice.html', {
            "customer_name": obj.customer_name,
            "date": obj.date,
            "memo_no": obj.memo_number,
            "items": product_context,
            "total": obj.total_price,
            "address": obj.address,
        })
        # Create a PDF
        css = CSS(string='''
            @page { 
                margin: 30px 30px; 
            } 
            '''
        )
        html = HTML(string=html_string)
        pdf = html.write_pdf(stylesheets=[css])

        # Create HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{obj.customer_name}_{obj.date}.pdf"'

        return response
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ProductRateAdmin(admin.ModelAdmin):
    list_display = ("product", "rate")
    list_editable = ("rate",)
    search_fields = ("product__name",)

class ProductInvoiceInline(admin.TabularInline):
    model = ProductInvoice
    autocomplete_fields = ("product",)
    readonly_fields = ("price", "product_rate")
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    inlines = (ProductInvoiceInline,)
    list_display = ("customer_name", "memo_number", "total_price", "date")
    readonly_fields = ("total_price",)

    actions = [generate_pdf]

    def save_formset(self, request, form, formset, change):
        formset.save()
        prices = form.instance.invoices.values_list("price", flat=True)
        form.instance.total_price = sum(prices)
        form.instance.save()
    
    # def save_related(self, request, form, formsets, change) -> None:
    #     breakpoint()
    #     super().save_related(request, form, formsets, change)
    #     # formsets.save()
    #     # prices = form.instance.invoices.values_list("price", flat=True)
    #     # form.instance.total_price = sum(prices)
    #     # form.instance.save()
        

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductRate, ProductRateAdmin)
# Register your models here.
