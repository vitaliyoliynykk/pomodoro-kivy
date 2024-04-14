from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout

Builder.load_file('components/circle_progress_bar.kv')

def hex_to_rgb(value, alpha=1):
    value = value.lstrip('#')
    return list(int(value[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + [alpha]

class CircleProgressBar(MDAnchorLayout):
    bar_color = ListProperty([163/255, 67/255, 67/255])
    # bar_color_secondary = ListProperty(hex_to_rgb('#A34343'))

    bar_width = NumericProperty(10)

    # circle progress in %
    progress = NumericProperty(10)
    status_text = StringProperty('00:00')

    def set_progress(self, value):
        self.progress = value
    
    def set_status_text(self, value):
        self.status_text = value
    
