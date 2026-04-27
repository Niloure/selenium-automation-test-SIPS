import pytest


@pytest.mark.protection
@pytest.mark.role_based
class TestRoleProtection:
    @pytest.mark.xfail(reason="Role protection not implemented yet")
    def test_user_page_forbidden_for_kepala_badan(self, login_as):
        dashboard = login_as("dzikri", "password")
        
        dashboard.driver.get(dashboard.base_url + "/user")
        
        assert "/user" not in dashboard.driver.current_url
    
    @pytest.mark.xfail(reason="Role protection not implemented yet")
    def test_user_page_forbidden_for_sekretaris(self, login_as):
        dashboard = login_as("saul", "password")
        
        dashboard.driver.get(dashboard.base_url + "/user")
        
        assert "/user" not in dashboard.driver.current_url
    
    @pytest.mark.xfail(reason="Role protection not implemented yet")
    def test_user_page_allowed_for_master_admin(self, login_as):
        dashboard = login_as("atala", "bko236cs72")
        
        dashboard.driver.get(dashboard.base_url + "/user")
        
        assert "/user" in dashboard.driver.current_url