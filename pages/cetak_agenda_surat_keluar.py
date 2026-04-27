from selenium.webdriver.common.by import By
from pages.base_cetakan_agenda import BaseCetakanAgenda
from datetime import datetime


class CetakanAgendaKeluar(BaseCetakanAgenda):
    INPUT_TGL_START = (By.ID, "input-cetak-agenda-start-date-surat-keluar")
    INPUT_TGL_END = (By.ID, "input-cetak-agenda-end-date-surat-keluar")