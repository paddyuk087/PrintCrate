from django.test import TestCase, Client
from products.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class TestCartView(TestCase):
    def client_setup(self):
        """Creates new client to conduct isolated unit tests."""
        self.client = Client()

    def test_redirect_with_empty_cart(self):
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, 302)

    def test_view_cart_contents(self):
        User.objects.create_user(
            username="testuser", password="thisisasecret101")
        item = Product(name="Product",
                       product_image="testing_img.jpg",
                       description="Product description.",
                       price="20.00",
                       stock_available="5",
                       showcase_product="True")
        item.save()
        self.client.login(username="testuser", password="thisisasecret101")
        session = self.client.session
        session["cart"] = {1: 1}
        session.save()
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, 200)

    def test_cart_correct_user_templates_rendered_with_call(self):
        """Tests if correct templates are rendered upon calling cart URL."""
        User.objects.create_user(
            username="testuser", password="thisisasecret101")
        item = Product(name="Product",
                       product_image="testing_img.jpg",
                       description="Product description.",
                       price="20.00",
                       stock_available="5",
                       showcase_product="True")
        item.save()
        self.client.login(username="testuser", password="thisisasecret101")
        session = self.client.session
        session["cart"] = {1: 1}
        session.save()
        response = self.client.get("/cart/")
        self.assertTemplateUsed(response, "cart.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "layout/head.html")
        self.assertTemplateUsed(response, "components/navbar.html")
        self.assertTemplateUsed(response, "components/cart-contents.html")
        self.assertTemplateUsed(response, "components/footer.html")
        self.assertTemplateUsed(response, "layout/scripts.html")
