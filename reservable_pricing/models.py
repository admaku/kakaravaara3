# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shoop.core.fields import MoneyValueField
from shoop.utils.properties import MoneyPropped, PriceProperty


class ReservableProductPrice(MoneyPropped, models.Model):
    product = models.ForeignKey("shoop.Product", related_name="+", on_delete=models.CASCADE)
    shop = models.ForeignKey("shoop.Shop", db_index=True, on_delete=models.CASCADE)
    group = models.ForeignKey("shoop.ContactGroup", db_index=True, on_delete=models.CASCADE)
    price = PriceProperty("price_value", "shop.currency", "shop.prices_include_tax")
    price_value = MoneyValueField()

    # TODO: (TAX) Check includes_tax consistency (see below)
    #
    # ReservableProductPrice entries in single shop should all have same
    # value of includes_tax, because inconsistencies in taxfulness of
    # prices may cause basket totals to be unsummable, since taxes are
    # unknown before customer has given their address and TaxfulPrice
    # cannot be summed with TaxlessPrice.

    class Meta:
        unique_together = (('product', 'shop', 'group'),)
        verbose_name = _(u"product price")
        verbose_name_plural = _(u"product prices")

    def __repr__(self):
        return "<ReservableProductPrice (p%s,s%s,g%s): price %s" % (
            self.product_id,
            self.shop_id,
            self.group_id,
            self.price,
        )