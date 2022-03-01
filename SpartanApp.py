from kivy.app import App
from sqlite3 import Error
from SpartanGrid import SpartanGrid
import sqlite3



class SpartanApp(App):

    def build(self):
        return SpartanGrid()