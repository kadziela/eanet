from django.test import SimpleTestCase
from django.urls import reverse, resolve
from controlling.views import (
    home, login_request, logout_request, administration_panel, employee_add,
    mpk_add, employee_list, mpk_list, worksheets_list, worksheet_edit
)


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_administration_panel_url_resolves(self):
        url = reverse('administration_panel')
        self.assertEquals(resolve(url).func, administration_panel)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_request)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_request)

    def test_employee_add_url_resolves(self):
        url = reverse('employee_add')
        self.assertEquals(resolve(url).func, employee_add)

    def test_mpk_add_url_resolves(self):
        url = reverse('mpk_add')
        self.assertEquals(resolve(url).func, mpk_add)

    def test_employee_list_url_resolves(self):
        url = reverse('employee_list')
        self.assertEquals(resolve(url).func, employee_list)

    def test_mpk_list_url_resolves(self):
        url = reverse('mpk_list')
        self.assertEquals(resolve(url).func, mpk_list)

    def test_worksheets_list_url_resolves(self):
        url = reverse('worksheets_list')
        self.assertEquals(resolve(url).func, worksheets_list)

    def test_worksheet_edit_url_resolves(self):
        url = reverse('worksheet_edit', args=['some-str'])
        self.assertEquals(resolve(url).func, worksheet_edit)
