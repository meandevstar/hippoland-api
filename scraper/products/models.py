from django.conf import settings

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    image_url = models.CharField(_("ImageUrl"), max_length=500)
    url = models.CharField(_("Url"), max_length=500)
    price = models.DecimalField(_("Price"), default=0, decimal_places=2, max_digits=10)
    sku = models.CharField(_("SKU"), max_length=255)
    description = models.CharField(_("Description"), max_length=10000)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        db_table = _("products")
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __unicode__(self):
        return smart_unicode(self.name)
