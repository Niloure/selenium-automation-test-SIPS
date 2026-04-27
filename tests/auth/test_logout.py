import pytest
from pages.dashboard_page import DashboardPage


@pytest.mark.auth
class TestLogout:
    def test_logout_master_admin(self, login_as):
        dashboard = login_as("atala", "bko236cs72")
        dashboard.logout()
        assert dashboard.is_redirected_to_login()
    
    def test_logout_admin(self, login_as):
        dashboard = login_as("arsyl", "password")
        dashboard.logout()
        assert dashboard.is_redirected_to_login()
    
    def test_logout_kepala_badan(self, login_as):
        dashboard = login_as("dzikri", "bko236cs72")
        dashboard.logout()
        assert dashboard.is_redirected_to_login()
    
    def test_logout_sekretaris_badan(self, login_as):
        dashboard = login_as("saul", "bko236cs72")
        dashboard.logout()
        assert dashboard.is_redirected_to_login()