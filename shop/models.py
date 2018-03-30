# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import pre_save

from mptt.models import MPTTModel, TreeForeignKey

from .utils import unique_slug_generator
from django.core.urlresolvers import reverse

PACKAGING =  (
            ('коробка', 'коробка',),
            ('упаковка', 'упаковка',),
            ('пачка', 'пачка',),
            ('рулон', 'рулон',),
            ('штука', 'штука',),
            ('мешок', 'мешок',),
            ('пара', 'пара',),
            ('блок', 'блок',),
        )
TYPEPRICE =    (
                    ('за коробку', 'за коробку',),
                    ('за упаковка', 'за упаковка',),
                    ('за пачку', 'за пачку',),
                    ('за рулон', 'за рулон',),
                    ('за штуку', 'за штуку',),
                    ('за мешок', 'за мешок',),
                    ('за пару', 'за пару',),
                    ('за блок', 'за блок',),
                )

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, db_index=True, default='page-slug', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ['name']
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def get_absolute_url_with_edit(self):
        return reverse('backapp:product_list_by_category_with_edit', args=[self.slug])


class Product(models.Model):
    category    = TreeForeignKey('Category', null=True, blank=True, db_index=True, related_name='cat', verbose_name=u"Категория")
    name        = models.CharField(max_length=200, db_index=True, verbose_name=u"Название")
    slug        = models.SlugField(max_length=200, db_index=True, default='page-slug', blank=True)
    image       = models.ImageField(upload_to='pic_of_product/',blank=True, null=True, default=None,
                                 verbose_name=u"Изображение товара")
    packaging   = models.CharField(choices = PACKAGING, max_length=20, verbose_name=u"Упаковка", blank=True, null=True, default=None)

    # description = models.TextField(blank=True, verbose_name="Описание")
    article     = models.CharField(max_length=13, db_index=True, default='0000000000000')
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"Цена")
    typeprice   = models.CharField(choices = TYPEPRICE, max_length=10, verbose_name=u"За какое кол-во указана цена", 
                                    blank=True, null=True, default=None)
    manufacture = models.CharField(max_length=20, verbose_name=u"Производитель", 
                                    blank=True, null=True, default=None)
    in_stock    = models.BooleanField(
                                    default  =True,
                                    db_index = True,
                                    verbose_name=u"в наличии")
    created     = models.DateTimeField(auto_now_add=True, db_index=True)
    updated     = models.DateTimeField(auto_now=True)
    popular     = models.BooleanField(
                        default = False,
                        verbose_name = 'в раздел "Популярные товары"')

    class Meta:
        ordering = ['name']
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'
        index_together = [
            ['id', 'slug']
        ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    def get_after_create_url(self):
        return reverse('backapp:product_detail_success', args=[self.pk, self.slug])

    def delete(self, *args, **kwargs):
        self.image.delete(save = False)
        super(Product, self).delete(*args, **kwargs)

def pre_save_receiver_page_model(sender, instance, *args, **kwargs):
	if instance.slug == 'page-slug' or instance.slug == '':
		instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver_page_model, sender=Category)
pre_save.connect(pre_save_receiver_page_model, sender=Product)