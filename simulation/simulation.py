from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import time

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='mesh', scale=(2500, 0, 2500), texture='grass')

editor_camera = EditorCamera(enabled=True, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.speed = 100

roads = Entity(model='resources\\3d_models\\roads.gltf', origin_y=-.5, scale=2,
               collider='box',
               shader=lit_with_shadows_shader
               )

# Lightning for better visibility
DirectionalLight(y=1.525, z=0, shadows=True)

Entity(model='resources\\3d_models\\e30.glb', origin_y=-.5, scale=5,
       position=(-85.67, 0.7, 56.99),
       rotation_y=270,
       collider='box'
       )


Entity(model='resources\\3d_models\\cst.glb', origin_y=-.5, scale=0.05,
       position=(-74.27, 1.24, 51.96),
       rotation_y=180,
       rotation_x=270,
       collider='box'
       )


# Traffic light system
class TrafficLight:
    def __init__(self, position, rotation_y):
        self.position = position
        self.rotation_y = rotation_y
        self.color = 'red'
        self.yellow_start_time = None
        self.yellow_duration = 2
        self.green_duration = 10

        # Create initial red light
        self.current_light = Entity(
            model='resources\\3d_models\\red_light.glb',
            origin_y=-.5,
            scale=10,
            position=position,
            rotation_y=rotation_y,
            collider='box'
        )

    def update(self):
        # Check if yellow light needs to switch to red
        if self.color == 'yellow' and self.yellow_start_time:
            if time.time() - self.yellow_start_time >= self.yellow_duration:
                if self.color == 'yellow':
                    self.switch_to_red()

    def trigger_yellow(self, next_color):
        if self.color != 'yellow':
            self.color = 'yellow'
            self.yellow_start_time = time.time()
            destroy(self.current_light)
            self.current_light = Entity(
                model='resources\\3d_models\\yellow_light.glb',
                origin_y=-.5,
                scale=10,
                position=self.position,
                rotation_y=self.rotation_y,
                collider='box'
            )
            invoke(self.switch_to_color, next_color, delay=self.yellow_duration)

    def switch_to_red(self):
        self.color = 'red'
        self.yellow_start_time = None
        destroy(self.current_light)
        self.current_light = Entity(
            model='resources\\3d_models\\red_light.glb',
            origin_y=-.5,
            scale=10,
            position=self.position,
            rotation_y=self.rotation_y,
            collider='box'
        )

    def switch_to_green(self):
        if self.color != 'green':
            self.trigger_yellow('green')

    def switch_to_color(self, next_color):
        destroy(self.current_light)
        if next_color == 'green':
            self.color = 'green'
            self.current_light = Entity(
                model='resources\\3d_models\\green_light.glb',
                origin_y=-.5,
                scale=10,
                position=self.position,
                rotation_y=self.rotation_y,
                collider='box'
            )
            invoke(self.trigger_yellow, 'red', delay=self.green_duration)
        elif next_color == 'red':
            self.switch_to_red()


# Create traffic lights
traffic_light = TrafficLight(position=(-52.7, -3.75, 62.18), rotation_y=180)
traffic_light2 = TrafficLight(position=(-72.45, -3.75, 52.45), rotation_y=270)
traffic_light3 = TrafficLight(position=(-72.45, -3.75, 71.90), rotation_y=90)

traffic_light4 = TrafficLight(position=(-72.45, -3.75, 189.44), rotation_y=0)
traffic_light5 = TrafficLight(position=(-52.7, -3.75, 199.40), rotation_y=90)
traffic_light6 = TrafficLight(position=(-52.7, -3.75, 179.50), rotation_y=270)

traffic_light7 = TrafficLight(position=(-52.7, -3.75, -65.28), rotation_y=180)
traffic_light8 = TrafficLight(position=(-72.45, -3.75, -75.00), rotation_y=270)
traffic_light9 = TrafficLight(position=(-72.45, -3.75, -55.50), rotation_y=90)

traffic_light10 = TrafficLight(position=(-72.45, -3.75, -193.89), rotation_y=0)
traffic_light11 = TrafficLight(position=(-52.7, -3.75, -203.7), rotation_y=270)
traffic_light12 = TrafficLight(position=(-52.7, -3.75, -183.7), rotation_y=270)


def update():
    # Update traffic light state
    if traffic_light:
        traffic_light.update()
        traffic_light2.update()
        traffic_light3.update()


def input(key):
    # If left-clicked, show the player's coordinates
    if held_keys['left mouse']:
        print_cords()

    # If right-clicked, switch traffic light to green
    if held_keys['right mouse']:
        traffic_light.switch_to_green()
        traffic_light2.switch_to_green()
        traffic_light3.switch_to_green()

    # If clicked '=' key, increase player's speed
    if key == '=':
        player.speed += 10

    # If clicked '-' key, decrease player's speed
    if key == '-':
        if player.speed > 0:
            player.speed -= 10

    # If clicked the esc key, turn off simulation
    if key == 'escape':
        exit()


# Printing player's current coordinates
def print_cords():
    print(f"Player's position: x={player.x:.2f}, y={player.y:.2f}, z={player.z:.2f}")


# Beautiful sky
Sky()

# Running the app
app.run()
