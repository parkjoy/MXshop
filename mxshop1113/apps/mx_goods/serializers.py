# coding=utf-8
from rest_framework import serializers
from mx_goods.models import Goods,GoodsCategory,GoodsImage,HotSearch,Banner,IndexAd,GoodsCategoryBrand

#三级类
class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#二级类
class GoodsCategorySerializer2(serializers.ModelSerializer):
    #三级类
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#一级类
class GoodsCategorySerializer(serializers.ModelSerializer):
    #二级类
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#轮播图序列化器
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


#list get 输出
class GoodsListSerializer(serializers.ModelSerializer):
    #嵌套序列化输出
    category = GoodsCategorySerializer()
    #分类id ---> 分类对象----> 序列化 ----->  赋值  category
    good_images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


#热搜
class HotSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearch
        fields = ("keywords",)


#轮播图
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


#商家
class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


#首页分类
class IndexGoodsSerializer(serializers.ModelSerializer):
    #二级类
    sub_cat = GoodsCategorySerializer2(many=True)
    #商家
    brands = GoodsCategoryBrandSerializer(many=True)
    #分类下商品
    goods = serializers.SerializerMethodField()
    #分类下的广告
    ad_goods = serializers.SerializerMethodField()


    def get_ad_goods(self,obj):
        #通过分类id，找到分类表中分分类广告
        index_ad = IndexAd.objects.filter(category_id=obj.id)
        if index_ad:
            goods_info = index_ad[0].goods
            goods_info_serializer = GoodsListSerializer(goods_info, many=False,context={"request": self.context["request"]}).data
            return goods_info_serializer



    def get_goods(self, obj):
        #通过分类找到分类下的所有商品
        from django.db.models import Q
        goods_info = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        #序列化
        goods_info_serializer = GoodsListSerializer(goods_info,many=True,context={"request":self.context["request"]}).data
        return goods_info_serializer



    class Meta:
        model = GoodsCategory
        fields = "__all__"

