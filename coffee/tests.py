from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CoffeeOrder, CoffeeVariety, Store


class OrderFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('customer', password='safe-password-123')
        self.staff_user = get_user_model().objects.create_user('store-staff', password='safe-password-123', is_staff=True)
        self.coffee = CoffeeVariety.objects.create(
            name='Test Espresso',
            image='coffees/test.jpg',
            type='EP',
            description='A test coffee.',
        )
        self.other_coffee = CoffeeVariety.objects.create(
            name='Test Mocha',
            image='coffees/mocha.jpg',
            type='MC',
            description='Another test coffee.',
        )
        self.store = Store.objects.create(name='Test Store', location='Test City')
        self.store.coffee_varieties.add(self.coffee)
        self.store.staff_members.add(self.staff_user)
        self.other_store = Store.objects.create(name='Other Store', location='Other City')
        self.other_store.coffee_varieties.add(self.other_coffee)

    def test_order_page_requires_login(self):
        response = self.client.get(reverse('order_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('order_create')}")

    def test_customer_can_send_valid_order_to_store(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('order_create'), {
            'coffee_variety': self.coffee.pk,
            'store': self.store.pk,
            'quantity': 2,
        })
        self.assertRedirects(response, reverse('my_orders'))
        order = CoffeeOrder.objects.get()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.store, self.store)
        self.assertEqual(order.quantity, 2)

    def test_order_rejects_coffee_not_served_by_store(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('order_create'), {
            'coffee_variety': self.other_coffee.pk,
            'store': self.store.pk,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not currently serve')
        self.assertEqual(CoffeeOrder.objects.count(), 0)

    def test_staff_sees_only_orders_for_assigned_stores(self):
        CoffeeOrder.objects.create(user=self.user, store=self.store, coffee_variety=self.coffee, quantity=1)
        CoffeeOrder.objects.create(user=self.user, store=self.other_store, coffee_variety=self.other_coffee, quantity=1)
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('store_orders'))
        self.assertContains(response, 'Test Espresso')
        self.assertNotContains(response, 'Test Mocha')

    def test_regular_customer_cannot_open_store_queue(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('store_orders'))
        self.assertEqual(response.status_code, 403)
