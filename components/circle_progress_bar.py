from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout

Builder.load_file('components/circle_progress_bar.kv')

class CircleProgressBar(MDAnchorLayout):
    bar_color = ListProperty([163/255, 67/255, 67/255])
    bar_width = NumericProperty(10)

    # circle progress in %
    progress = NumericProperty(1)
    status_text = StringProperty('00:00')

    def set_progress(self, value):
        self.progress = value
    
    def set_status_text(self, value):
        self.status_text = value
    
