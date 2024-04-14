from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from components.circle_progress_bar import CircleProgressBar
from kivy.lang import Builder


Builder.load_file('screens/timer.kv')

# from .progress_bar import SemiCircleProgressBar

class TimerWidget(GridLayout):
    def __init__(self, max_time=1, **kwargs):
        super().__init__(**kwargs)
        self.max_time = max_time * 60  # Convert to seconds
        self.current_time = self.max_time
        self._timer_event = None
        self.timer_label = '00:00'

    def start_timer(self, instance):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        else:
            self._timer_event = Clock.schedule_interval(self.update_timer, 1)
        instance.set_status_text('test')

    def update_timer(self, dt):
        self.current_time -= 1
        if self.current_time <= 0:
            self.reset_timer()
            return
        minutes, seconds = divmod(self.current_time, 60)
        self.timer_label = f"{minutes:02d}:{seconds:02d}"
        self.timer_instance.set_status_text(self.timer_label)
        self.timer_instance.set_progress(self.current_time/(self.max_time /100))

    def skip_timer(self):
        self.reset_timer()

    def reset_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
        self.current_time = self.max_time
        minutes, seconds = divmod(self.current_time, 60)
        self.timer_label.text = f"{minutes:02d}:{seconds:02d}"
        self.start_button.text = 'Start'
    
    def on_start_pressed(self, instance):
        self.start_timer(instance)
        self.timer_instance = instance