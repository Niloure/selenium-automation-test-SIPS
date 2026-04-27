import pytest


@pytest.mark.visibility
class TestMenuVisibility:
    @pytest.mark.parametrize(
        "username,password,should_visible",
        [
            ("atala", "bko236cs72", True),     # Master Admin
            ("arsyl", "password", False),      # Admin
            ("dzikri", "bko236cs72", False),   # Kepala Badan
            ("saul", "bko236cs72", False),     # Sekretaris
        ],
        ids=["master_admin", "admin", "kepala_badan", "sekretaris"]
    )
    def test_manage_user_visibility(self, login_as, username, password, should_visible):
        dashboard = login_as(username, password)
        assert dashboard.is_manage_user_visible() == should_visible
    
    @pytest.mark.parametrize(
        "username,password,menu_text,should_visible",
        [
            ("atala", "bko236cs72", "Catatan Surat", False),
            ("atala", "bko236cs72", "Klasifikasi Surat", False),
            ("atala", "bko236cs72", "Buku Agenda", False),
            ("arsyl", "password", "Catatan Surat", True),
            ("arsyl", "password", "Klasifikasi Surat", True),
            ("arsyl", "password", "Buku Agenda", False),
            ("dzikri", "bko236cs72", "Catatan Surat", True),
            ("dzikri", "bko236cs72", "Klasifikasi Surat", False),
            ("dzikri", "bko236cs72", "Buku Agenda", True),
            ("saul", "bko236cs72", "Catatan Surat", True),
            ("saul", "bko236cs72", "Klasifikasi Surat", False),
            ("saul", "bko236cs72", "Buku Agenda", True),
        ],
        ids=[
            "master_admin_catatan_surat", "master_admin_klasifikasi", "master_admin_buku_agenda",
            "admin_catatan_surat", "admin_klasifikasi", "admin_buku_agenda",
            "kepala_badan_catatan_surat", "kepala_badan_klasifikasi", "kepala_badan_buku_agenda",
            "sekretaris_catatan_surat", "sekretaris_klasifikasi", "sekretaris_buku_agenda"
        ]
    )
    def test_menu_visibility_by_role(self, login_as, username, password, menu_text, should_visible):
        dashboard = login_as(username, password)
        assert dashboard.is_menu_visible(menu_text) == should_visible