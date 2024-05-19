from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="product")

    def __str__(self) -> str:
        return self.name

class ProductRate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_rates", verbose_name="product")
    rate = models.IntegerField(verbose_name="rate")

    def __str__(self) -> str:
        return self.product.name

class Invoice(models.Model):
    customer_name = models.CharField(verbose_name="customer name", max_length=150)
    address = models.CharField(verbose_name="address", max_length=250)
    memo_number = models.IntegerField(verbose_name="memo number")
    date = models.DateField()
    total_price = models.IntegerField(blank=True, null=True, verbose_name="total price")

class ProductInvoice(models.Model):
    product = models.ForeignKey(ProductRate, on_delete=models.PROTECT, related_name="product_invoices", verbose_name="product")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoices", verbose_name="invoice")
    quantity = models.PositiveIntegerField(verbose_name="quantity")
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="price")

    def save(self, *args, **kwargs):
        self.price = self.product.rate * self.quantity
        return super().save(*args, **kwargs)
