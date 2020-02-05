from rest_framework.test import APITestCase
from .models import *
from . import serializers
from rest_framework.test import APIClient
from django.core.management import call_command
from pprint import pprint
import datetime
import json
from django.db.models import Q
import random


class DefaultTestMixin:
    @classmethod
    def setUpTestData(cls):
        from run_init import main
        main()
        cls.noauth_client = APIClient()
        cls.superauth_client = APIClient()
        cls.superauth_client.credentials(HTTP_AUTHORIZATION='Token ' + '1111')


class TestBanner(DefaultTestMixin, APITestCase):
    # todo not yet
    response_keys = ['id', 'bigimage', 'smallimage', 'link', 'queue', 'status', 'display_type', 'start_time',
                     'end_time', 'content']
    contents = [
        dict(
            language_type=1,
            title='title_CH',
            subtitle='subtitle_CH',
            description='description_CH',
            button='button_CH',
        ),
        dict(
            language_type=2,
            title='title_EN',
            subtitle='subtitle_EN',
            description='description_EN',
            button='button_EN',
        )
    ]

    def test_banner_list(self):
        url = '/api/banner/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        item = r.data[0]
        self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_banner_post(self):
        url = '/api/banner/'
        data = dict(
            bigimage='default-banner-bigimage.png',
            smallimage='default-banner-smallimage.png',
            link='http://ezgo-buy.com/',
            queue=1,
            status=True,
            display_type=False,
            start_time='2019-06-20',
            end_time='2019-09-20',
            content=self.contents
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

        item = r.data
        self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_banner_update(self):
        instance = Banner.objects.first()
        url = f'/api/banner/{instance.id}/'
        data = dict(
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        item = r.data
        self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_banner_delete(self):
        instance = Banner.objects.first()
        url = f'/api/banner/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 200)


class TestPermission(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'name', 'description', 'role_manage', 'member_manage', 'order_manage', 'banner_manage',
                     'catalog_manage', 'product_manage', 'coupon_manage']

    def test_permission_list(self):
        url = '/api/permission/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_noauth_permission_list(self):
        url = '/api/permission/'
        r = self.noauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 401)

    def test_permission_post(self):
        url = '/api/permission/'
        i = random.randint(1, 10)
        data = dict(
            name='打打醬油',
            description='路過路過',
            role_manage=2,
            member_manage=2,
            order_manage=2,
            banner_manage=2,
            catalog_manage=2,
            product_manage=2,
            coupon_manage=2
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)
        # request = reqponse
        for key in data:
            self.assertEqual(data[key], r.data[key])
        # response permission keys mapping
        self.assertEqual(sorted(list(r.data.keys())), sorted(self.response_keys))

    def test_permission_update(self):
        instance = Permission.objects.filter(highest_permission=False).last()
        url = f'/api/permission/{instance.id}/'
        data = dict(
            name='打打打醬油',
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        # return check
        for key in data:
            self.assertEqual(data[key], r.data[key])

    def test_permission_has_manager_delete_error(self):
        instance = Permission.objects.filter(highest_permission=False).last()
        url = f'/api/permission/{instance.id}/'
        # 確認 update 可以
        data = dict(
            name='打打打打醬油',
            description='路過路過',
            role_manage=2,
            member_manage=2,
            order_manage=2,
            banner_manage=2,
            catalog_manage=2,
            product_manage=2,
            coupon_manage=2
        )
        r = self.superauth_client.put(url, data)
        self.assertEqual(r.status_code, 200)

        # 確認不能 delete
        # todo
        r = self.superauth_client.delete(url)
        self.assertEqual(r.status_code, 400)

    def test_permission_cantdelete(self):
        instance = Permission.objects.filter(highest_permission=False).first()
        url = f'/api/permission/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        # todo
        self.assertEqual(r.status_code, 400)
        # type dict
        self.assertIsInstance(r.data, dict)

    def test_permission_highest_permission(self):
        # if highest_permission = True cant update, delete
        instance = Permission.objects.filter(highest_permission=True).first()
        url = f'/api/permission/{instance.id}/'
        data = dict(
            deleted_status=True
        )
        r = self.superauth_client.put(url, data)
        # status 400
        self.assertEqual(r.status_code, 400)


class TestManager(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'permission_name', 'permission_description', 'email', 'cn_name', 'en_name', 'remarks',
                     'status',
                     'permission']

    def test_manager_list(self):
        url = '/api/manager/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_manager_post(self):
        url = '/api/manager/'
        number = random.choices(range(9), k=9)
        number = ''.join(map(str, number))
        permission = Permission.objects.last()
        data = dict(
            email='ma11x@conquers.co',
            password=f'a{number}',
            status=True,
            cn_name='肉球',
            en_name='Meatball',
            permission=permission.id
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

    def test_manager_post_password_validate_error(self):
        url = '/api/manager/'
        number = random.choices(range(9), k=9)
        number = ''.join(map(str, number))
        permission = Permission.objects.last()
        data = dict(
            email='ma22x@conquers.co',
            password=f'{number}',
            status=True,
            cn_name='肉球',
            en_name='Meatball',
            permission=permission
        )
        r = self.superauth_client.post(url, data)
        # status 400
        self.assertEqual(r.status_code, 400)

    def test_manager_update(self):
        instance = Manager.objects.filter(permission__highest_permission=False).first()
        url = f'/api/manager/{instance.id}/'
        data = dict(
            status=False,
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        # return check

    def test_manager_delete(self):
        instance = Manager.objects.filter(permission=2).first()
        url = f'/api/manager/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)
        # type dict

    def test_manager_highest_permission(self):
        # if highest_permission = True cant update, delete
        instance = Manager.objects.filter(permission__highest_permission=True).first()
        url = f'/api/manager/{instance.id}/'
        r = self.superauth_client.delete(url)
        # status 400
        # todo
        self.assertEqual(r.status_code, 400)

    def test_manager_update_password_check(self):
        instance = Manager.objects.filter(permission__highest_permission=False).last()
        new_psw = 'a123456'
        url = f'/api/manager/{instance.id}/'
        data = dict(password=new_psw)
        r = self.superauth_client.put(url, data)
        # check response no password
        self.assertIsNone(r.data.get('password'))
        instance = Manager.objects.get(pk=instance.id)
        self.assertNotEqual(new_psw, instance.password)


class TestMember(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'member_number', 'returns', 'account', 'join_at', 'name', 'phone', 'cellphone', 'remarks',
                     'status']

    def test_member_list(self):
        url = '/api/member/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_member_reed(self):
        instnace = Member.objects.first()
        url = f'/api/member/{instnace.id}/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # check response list
        self.assertEqual(list(r.data),
                         self.response_keys)

    def test_member_post(self):
        url = '/api/member/'
        number = random.choices(range(9), k=9)
        number = ''.join(map(str, number))
        data = dict(
            name="康大闓",
            account=f"test{number}@conquers.co",
            phone=f"{number}",
            remarks='test',
            password='1111wqwqw',
            status=True
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

    def test_member_update(self):
        instance = Member.objects.first()
        url = f'/api/member/{instance.id}/'
        data = dict(
            name="品管人員",
            phone='121212'
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        # return check
        for key in data:
            self.assertEqual(data[key], r.data[key])

    def test_member_delete(self):
        instance = Member.objects.first()
        url = f'/api/member/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)


class TestCategory(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'sub_categories', 'name', 'image_url', 'main_category']

    def test_category_list(self):
        url = '/api/category/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_category_list_noauth(self):
        url = '/api/category/'
        r = self.noauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_category_reed(self):
        instance = Category.objects.first()
        url = f'/api/category/{instance.id}/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # check response list
        self.assertEqual(list(r.data),
                         self.response_keys)

    def test_category_post(self):
        url = '/api/category/'
        data = dict(
            name='分類',
            image_url='c-01.svg',
            main_category=1
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

    def test_category_update(self):
        instance = Category.objects.first()
        url = f'/api/category/{instance.id}/'
        data = dict(
            name="品管人員",
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        # return check
        for key in data:
            self.assertEqual(data[key], r.data[key])

    def test_category_delete(self):
        instance = Category.objects.first()
        url = f'/api/category/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)


class TestTag(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'tag_image_image_url', 'products', 'name', 'tag_image']

    def test_tag_list(self):
        import time
        url = '/api/tag/'
        tStart = time.time()
        for i in range(10):
            r = self.superauth_client.get(url)
        tEnd = time.time()
        print((tEnd - tStart) / 10)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertEqual(list(item.keys()),
                         self.response_keys)

    def test_tag_reed(self):
        instance = Tag.objects.first()
        url = f'/api/tag/{instance.id}/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # check response list
        self.assertEqual(list(r.data),
                         self.response_keys)

    def test_tag_post(self):
        # create product_ids
        url = '/api/tag/'
        product_ids = list(set(map(lambda o: o.id, random.choices((Product.objects.filter(tag__isnull=True)), k=10))))
        tag_image = random.choice(TagImage.objects.all())
        data = dict(
            name='分類',
            product_ids=product_ids,
            tag_image=tag_image.id
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)
        # check 數量一致
        tag_id = r.data['id']
        self.assertEqual(len(product_ids), Product.objects.filter(tag=tag_id, id__in=product_ids).count())

        # check validate
        product_ids.append(Product.objects.filter(tag__isnull=False).first().id)
        data['product_ids'] = product_ids
        r = self.superauth_client.post(url, data)
        self.assertEqual(r.status_code, 400)

    def test_tag_update(self):
        instance = Tag.objects.first()
        url = f'/api/tag/{instance.id}/'
        product_ids = list(set(map(lambda o: o.id, random.choices((Product.objects.filter(tag__isnull=True)), k=10))))
        data = dict(
            name="品管人員",
            product_ids=product_ids
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        tag_id = r.data['id']
        self.assertEqual(len(product_ids), Product.objects.filter(tag=tag_id, id__in=product_ids).count())

        # return check
        for key in data:
            if key == 'product_ids':
                continue
            self.assertEqual(data[key], r.data[key])

        product_ids.append(Product.objects.filter(tag__isnull=False).first().id)
        data['product_ids'] = product_ids
        r = self.superauth_client.put(url, data)
        self.assertEqual(r.status_code, 400)

    def test_tag_delete(self):
        instance = Tag.objects.first()
        url = f'/api/tag/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)


class TestBrand(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'en_name', 'cn_name', 'index', 'menu', 'image_url', 'fake_id']

    def test_brand_list(self):
        url = '/api/brand/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        # request = reqponse
        item = r.data[0]
        self.assertIsInstance(item['children'], list)
        item = item['children'][0]
        self.assertEqual(list(item.keys()), self.response_keys)

    def test_brand_reed(self):
        instance = Tag.objects.first()
        url = f'/api/brand/{instance.id}/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # check response list
        self.assertEqual(list(r.data),
                         self.response_keys)

    def test_brand_post(self):
        tagimage = TagImage.objects.first()
        url = '/api/brand/'
        data = dict(
            cn_name='tagimage',
            en_name='分類',
            index=True,
            image_url='213'
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

    def test_brand_update(self):
        instance = Tag.objects.first()
        url = f'/api/brand/{instance.id}/'
        data = dict(
            cn_name="品管人員",
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        # return check
        for key in data:
            self.assertEqual(data[key], r.data[key])

    def test_brand_delete(self):
        instance = Tag.objects.first()
        url = f'/api/brand/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)


class TestProduct(DefaultTestMixin, APITestCase):
    response_keys = ['id', 'product_number', 'brand_en_name', 'brand_cn_name', 'category_name', 'name', 'title',
                     'sub_title',
                     'weight', 'price', 'fake_price', 'inventory_status', 'description', 'description_2', 'brand',
                     'tag',
                     'category', 'productimages', 'specifications']

    def test_product_list(self):
        url = '/api/product/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        item = r.data[0]
        self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_product_post(self):
        url = '/api/product/'
        data = dict(
            product_number=222,
            brand=1,
            name=222,
            title=222,
            sub_title=222,
            weight=222,
            price=222,
            fake_price=222,
            inventory_status=222,
            description=222,
            description_2=222,
            tag=1,
            category=1,
            specification=[
                {
                    "name": "213"
                }
            ],
            productimage=[
                {
                    "main_image": True,
                    "image_url": "23132222"
                }
            ]
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

    def test_product_update(self):
        instance = Product.objects.first()
        url = f'/api/product/{instance.id}/'
        data = dict(
            product_number=2222,
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)

    def test_product_delete(self):
        instance = Product.objects.first()
        url = f'/api/product/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)


class TestCart(DefaultTestMixin, APITestCase):
    response_keys = []

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        product = Product.objects.first()
        data = dict(
            product=product,
            specification=product.specifications.first(),
            quantity=1
        )
        member = Member.objects.filter(account='max@conquers.co').first()
        instance = Cart.objects.create(**data, member=member)

    def test_cart_list(self):
        url = '/api/cart/'
        r = self.superauth_client.get(url)
        # status 200
        self.assertEqual(r.status_code, 200)
        # response type
        self.assertIsInstance(r.data, list)
        item = r.data[0]
        # todo 別的user 可否可以看到該cart
        # todo
        # self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_cart_post(self):
        url = '/api/cart/'
        product = Product.objects.first()
        data = dict(
            product=product.id,
            specification=product.specifications.first().id,
            quantity=1
        )
        r = self.superauth_client.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)

        item = r.data
        # todo
        # self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_cart_update(self):
        instance = Cart.objects.first()
        url = f'/api/cart/{instance.id}/'
        data = dict(
            quantity=2
        )
        r = self.superauth_client.put(url, data)
        # status 200
        self.assertEqual(r.status_code, 200)
        # type dict
        self.assertIsInstance(r.data, dict)
        item = r.data
        # todo
        # self.assertEqual(set(item.keys()), set(self.response_keys))

    def test_cart_delete(self):
        instance = Cart.objects.first()
        url = f'/api/cart/{instance.id}/'
        r = self.superauth_client.delete(url)
        # stauts 200
        self.assertEqual(r.status_code, 204)
