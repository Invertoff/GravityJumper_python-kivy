from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget

# Set minimum resolution to Full HD
Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '1920')

# Allow resizing the window for testing
Config.set('graphics', 'resizable', '1')

class Player(Widget):
    def __init__(self, scale_factor=1.0, **kwargs):
        super().__init__(**kwargs)
        self.size = (40 * scale_factor, 40 * scale_factor)
        self.pos = (Window.width // 3 - self.size[0] // 2, Window.height // 2 - self.size[1] // 2)
        self.velocity_y = 0
        self.gravity = -0.5 * scale_factor
        self.jump_strength = 17 * scale_factor

        with self.canvas:
            Color(0, 0, 1, 1)  # Blue color
            self.circle = Ellipse(pos=self.pos, size=self.size)

    def update(self, dt):
        # Apply gravity
        self.velocity_y += self.gravity
        new_y = self.y + self.velocity_y

        # Check window borders
        if new_y < 0:
            new_y = 0
            self.velocity_y = 0
        elif new_y + self.height > Window.height:
            new_y = Window.height - self.height
            self.velocity_y = 0

        self.y = new_y
        self.circle.pos = (self.x, self.y)

    def jump(self):
        self.velocity_y = self.jump_strength


class GravityJumperGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale_factor = min(Window.width / 1080, Window.height / 1920)
        self.player = Player(scale_factor=self.scale_factor)
        self.add_widget(self.player)

        # Schedule updates
        Clock.schedule_interval(self.update, 1 / 60)

        # Bind window resize
        Window.bind(on_resize=self.on_window_resize)

    def update(self, dt):
        self.player.update(dt)

    def on_touch_down(self, touch):
        self.player.jump()

    def on_window_resize(self, window, width, height):
        self.scale_factor = min(width / 1080, height / 1920)
        self.player.size = (40 * self.scale_factor, 40 * self.scale_factor)
        self.player.circle.size = self.player.size
        self.player.circle.pos = (self.player.x, self.player.y)


class GravityJumperApp(App):
    def build(self):
        return GravityJumperGame()


if __name__ == "__main__":
    GravityJumperApp().run()
