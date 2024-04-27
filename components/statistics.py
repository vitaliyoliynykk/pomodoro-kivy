from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField

Builder.load_file('components/statistics.kv')

class DialogContent(BoxLayout):
    pass


class Statistics(MDAnchorLayout):
    primary_color = ListProperty([163/255, 67/255, 67/255])
    secondary_color = ListProperty([192/255, 214/255, 232/255])
    title = StringProperty('Pomodoro')
    goal = 5
    completed = 0
    completed_label = StringProperty('{}/{} completed today'.format(completed, goal))
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_statistics()

    def set_title(self, title):
        self.title = title

    def update_statistics(self):
        self.completed = self.get_from_state('completed')
        self.goal = self.get_from_state('goal')
        self.completed_label = '{}/{} completed today'.format(self.completed, self.goal)

    def get_from_state(self, key):
            store = JsonStore('statistic_store.json')

            return store.get(self.get_current_date()).get(key) or 0

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Set yoour goal for today",
                content_cls=MDTextField(input_filter='int'),
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="SET",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.on_set_goal
                    ),
                ],
            )

        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def on_set_goal(self, *args):
        field_content = self.dialog.content_cls

        store = JsonStore('statistic_store.json')
        store.put(self.get_current_date(), goal=int(field_content.text))
        
        self.dialog.dismiss()
        self.update_statistics()
    
    def get_current_date(self):
            current_date = datetime.now()
            return  current_date.strftime('%Y-%m-%d')