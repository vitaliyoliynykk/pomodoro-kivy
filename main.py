from kivymd.app import MDApp
from screens.timer import TimerWidget
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

# from kivymd.uix.boxlayout import MDBoxLayout

statistic_store = JsonStore('statistic_store.json')

# class ContentNavigationDrawer():
#     pass

class MainApp(MDApp):
    def build(self):
        # Iphone 14 Pro dimensions
        Window.size = (430,932)
        self.init_storage()

        return MDFloatLayout()
    
    def init_storage(self):
        current_date = datetime.now()
        current_formatted_date = current_date.strftime('%Y-%m-%d')

        if (not statistic_store.exists(current_formatted_date)):
            statistic_store.put(current_formatted_date, completed=0, goal='null', goal_text='null')


if __name__ == '__main__':
    MainApp().run()