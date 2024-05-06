from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

Builder.load_file('components/statistics.kv')

class GoalDialogContent(BoxLayout):
    pass

class SettingsDialogContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.populate_form, 0.1)

    def populate_form(self, dt):
        store = JsonStore('settings_store.json')

        focus_time = store.get('cycles').get('focus')
        rest_time = store.get('cycles').get('rest')
        rest_long_time = store.get('cycles').get('rest_long')

        self.ids.focus_input.text = str(focus_time)
        self.ids.rest_input.text = str(rest_time)
        self.ids.long_rest_input.text = str(rest_long_time)


class Statistics(MDAnchorLayout):
    primary_color = ListProperty([163/255, 67/255, 67/255])
    secondary_color = ListProperty([192/255, 214/255, 232/255])
    title = StringProperty('Pomodoro')
    goal_visible = BooleanProperty(False)
    completed_label = StringProperty('#0 of 0')

    goal = 5
    completed = 0
    goal_dialog = None
    settings_dialog = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_statistics()
        Clock.schedule_once(self.init_menu, 0.5)


    def init_menu(self, dt):
        menu_items = [
            {
                "text": "Set a goal",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.show_goal_dialog()
            },
            {
                "text": "Settings",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.show_settings_dialog()
            },
            {
                "text": "Reset goal and statistics",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.reset_statistics()
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.button,
            items=menu_items,
            width_mult=4,
        )

    def set_title(self, title):
        self.title = title

    def update_statistics(self):
        self.completed = self.get_from_state('completed')
        self.goal = self.get_from_state('goal')
        self.goal_text = self.get_from_state('goal_text')
        self.goal_visible = self.goal != 'null' and self.goal_text != 'null'
        self.completed_label = '{}: #{} of {}'.format(self.goal_text, self.completed, self.goal)

    def get_from_state(self, key):
            store = JsonStore('statistic_store.json')

            return store.get(self.get_current_date()).get(key) or 0

    def show_goal_dialog(self):
        self.menu.dismiss()

        if not self.goal_dialog:
            self.goal_dialog = MDDialog(
                title="Set yoour goal for today",
                content_cls=GoalDialogContent(),
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_goal_dialog
                    ),
                    MDFlatButton(
                        text="SET",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.on_set_goal
                    ),
                ],
            )

        self.goal_dialog.open()

    def show_settings_dialog(self):
        self.menu.dismiss()

        if not self.settings_dialog:
            self.settings_dialog = MDDialog(
                title="Settings",
                content_cls=SettingsDialogContent(),
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_settings_dialog
                    ),
                    MDFlatButton(
                        text="SET",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.on_set_settings
                    ),
                ],
            )

        self.settings_dialog.open()

    def close_goal_dialog(self, *args):
        self.goal_dialog.dismiss()

    def close_settings_dialog(self, *args):
        self.settings_dialog.dismiss()

    
    def on_set_settings(self, e):
        dialog_content = self.settings_dialog.content_cls

        focus_time = dialog_content.ids.focus_input
        rest_time = dialog_content.ids.rest_input
        long_rest_time = dialog_content.ids.long_rest_input

        self.validate_field(focus_time)
        self.validate_field(rest_time)
        self.validate_field(long_rest_time)

        if focus_time.text.strip() and rest_time.text.strip() and long_rest_time.text.strip():
            store = JsonStore('settings_store.json')
            store.put('cycles', focus=int(focus_time.text), rest=int(rest_time.text), rest_long=int(long_rest_time.text))

            self.settings_dialog.dismiss()
        

    def on_set_goal(self, *args):
        dialog_content = self.goal_dialog.content_cls

        number_of_pomodoros = dialog_content.ids.number_input
        goal_text = dialog_content.ids.goal_input

        self.validate_field(number_of_pomodoros)
        self.validate_field(goal_text)

        if number_of_pomodoros.text.strip() and goal_text.text.strip():
            store = JsonStore('statistic_store.json')
            current_state = store.get(self.get_current_date())
            store.put(self.get_current_date(), goal=int(number_of_pomodoros.text), goal_text=goal_text.text, completed=current_state.get('completed'))
        
            self.goal_dialog.dismiss()
            self.update_statistics()
    
    def get_current_date(self):
            current_date = datetime.now()
            return  current_date.strftime('%Y-%m-%d')
    
    def validate_field(self, field):
        if not field.text.strip():
            field.error = True
        else:
            field.error = False

    def reset_statistics(self):
        store = JsonStore('statistic_store.json')
        store.put(self.get_current_date(), goal='null', goal_text='null', completed=0)
        self.update_statistics()
        self.menu.dismiss()