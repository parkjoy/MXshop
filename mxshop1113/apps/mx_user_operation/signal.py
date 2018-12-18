# coding=utf-8
from mx_user_operation.models import UserFav
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        #获取商品
        goods = instance.goods
        #数量+1
        goods.fav_num +=1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    #获取商品
    goods = instance.goods
    #数量-1
    goods.fav_num -=1
    goods.save()