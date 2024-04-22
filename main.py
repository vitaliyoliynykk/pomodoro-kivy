from kivy.app import App
from kivymd.app import MDApp
from screens.timer import TimerWidget
from components.circle_progress_bar import CircleProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

statistic_store = JsonStore('statistic_store.json')

class MainApp(MDApp):
    def build(self):
        # Iphone 14 Pro dimensions
        Window.size = (430,932)
        self.init_storage()

        return MDFloatLayout()
    
    def init_storage(self):
        if (statistic_store.keys() == []):
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')

            statistic_store.put(formatted_date, completed=0)


if __name__ == '__main__':
    MainApp().run()