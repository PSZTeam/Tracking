from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from plyer import accelerometer


class AccelerometerTest(BoxLayout):
    def __init__(self):
        super(AccelerometerTest, self).__init__()
        self.sensorEnabled = False
        self.f = open('data.csv', 'w')
        self.f.write('X,Y,Z\n')

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)
                self.f.close()
                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])

            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])

            self.f.write(str(val[0]) + ',' + str(val[1]) + ',' + str(val[2]) + '\n')


class AccelerometerTestApp(App):
    def build(self):
        return AccelerometerTest()

    def on_pause(self):
        return True


if __name__ == '__main__':
    AccelerometerTestApp().run()