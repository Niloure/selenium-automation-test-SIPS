import pytest
from pages.dashboard_page import DashboardPage

@pytest.mark.positive
@pytest.mark.auth
class TestLoginPositive:
    def test_login_valid_credentials(self, login_as, all_role_creds):
        username, password = all_role_creds
        dashboard = login_as(username, password)
        assert dashboard.is_element_visible(dashboard.DASHBOARD_TITLE)
    
    # jika ingin lebih eksplisit untuk masing-masing role, bisa juga:
    # def test_login_master_admin(self, login_as, master_admin_creds):
    #     username, password = master_admin_creds
    #     dashboard = login_as(username, password)
    #     assert dashboard.is_element_visible(dashboard.DASHBOARD_TITLE)
    #
    # def test_login_admin(self, login_as, admin_creds):
    #     username, password = admin_creds
    #     dashboard = login_as(username, password)
    #     assert dashboard.is_element_visible(dashboard.DASHBOARD_TITLE)
    # ... dan seterusnya