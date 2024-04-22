from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout

Builder.load_file('components/statistics.kv')

class Statistics(MDAnchorLayout):
    primary_color = ListProperty([163/255, 67/255, 67/255])
    title = StringProperty('Pomodoro')

    def set_title(self, title):
        self.title = title