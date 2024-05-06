from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

Builder.load_file('screens/timer.kv')

class TimerWidget(GridLayout):
    sequence = [{'time': 25, 'type': 'focus'}, 
                {'time': 5, 'type': 'rest'},
                {'time': 25, 'type': 'focus'},
                {'time': 5, 'type': 'rest'},
                {'time': 25, 'type': 'focus'},
                {'time': 15, 'type': 'rest'}]
    
    primary_color = ListProperty([163/255, 67/255, 67/255])
    blue_color = ListProperty([192/255, 214/255, 232/255])
    skip_disabled = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.iteration = 0
        self.max_iteration = 5

        self.set_max_time()
        self.current_time = self.max_time
        self._timer_event = None
        self.skip_disabled = True


    def toggle_timer(self):
        self.update_statistics_component()

        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
            self.ids.start_button.text = 'Start'
        else:
            self._timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.ids.start_button.text = 'Pause'
            self.skip_disabled = False

    def update_timer(self, dt):
        self.current_time -= 1
        if self.current_time <= 0:
            self.reset_timer()
            return
        self.update_progress_bar()

    def skip_timer(self):
        self.reset_timer()
        self.skip_disabled = True

    def reset_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

        self.update_storage()
        self.calculate_iterations()
        self.update_statistics_component()
        self.set_max_time()
        self.current_time = self.max_time
        self.update_progress_bar()
        
        
        self.ids.start_button.text = 'Start'

    def update_progress_bar(self):
        minutes, seconds = divmod(self.current_time, 60)
        self.timer_label = f"{minutes:02d}:{seconds:02d}"
        self.ids.progress_bar.set_status_text(self.timer_label)
        self.ids.progress_bar.set_progress(100 - self.current_time/(self.max_time /100))
    
    def update_statistics_component(self):
        if (self.sequence[self.iteration].get('type') == 'focus'):
            self.ids.statistics.set_title('Time to focus')
        else:
            self.ids.statistics.set_title('Time to rest')
            self.ids.statistics.update_statistics()
    
    def set_max_time(self):
        self.max_time = self.sequence[self.iteration].get('time') * 60  # Max time in seconds
    
    def calculate_iterations(self):
        self.iteration +=1

        if self.iteration > self.max_iteration:
            self.iteration = 0
    
    def update_storage(self):
        if (self.sequence[self.iteration].get('type') == 'focus'):
            store = JsonStore('statistic_store.json')

            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')
    
            current_state = store.get(formatted_date)

            completed = current_state.get('completed') or 0
            completed +=1

            store.put(formatted_date, completed=completed, goal=current_state.get('goal'), goal_text=current_state.get('goal_text'))