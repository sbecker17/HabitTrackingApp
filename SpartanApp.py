from kivy.app import App
from LoginPage import LoginPage

class SpartanApp(App):

    def build(self):
        return LoginPage()