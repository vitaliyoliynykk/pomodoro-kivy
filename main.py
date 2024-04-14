from kivy.app import App
from kivymd.app import MDApp
from screens.timer import TimerWidget
from components.circle_progress_bar import CircleProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window


class MainApp(MDApp):
    def build(self):
        # Iphone 14 Pro dimensions
        Window.size = (430,932)

        return MDFloatLayout()


if __name__ == '__main__':
    MainApp().run()