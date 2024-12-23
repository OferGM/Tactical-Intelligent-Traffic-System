from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import time

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='mesh', scale=(974, 0, 1221), texture='grass')

editor_camera = EditorCamera(enabled=True, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.speed = 100

roads = Entity(model='resources\\3d_models\\new_roads.glb', origin_y=-.5, origin_x=-.25, origin_z=-1.5, scale=2,
               collider='box',
               shader=lit_with_shadows_shader
               )

# Lightning for better visibility
DirectionalLight(y=1.525, z=0, shadows=True)

car = Entity(model='resources\\3d_models\\e30.glb', origin_y=-.5, scale=5,
             position=(-77.85, 0.7, 64.05),
             rotation_y=270,
             collider='box'
             )

passenger = Entity(model='resources\\3d_models\\cst.glb', origin_y=-.5, scale=0.05,
                   position=(-74.40, 1.24, 55.20),
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
traffic_light1 = TrafficLight(position=(-52.40, -3.75, 65.20), rotation_y=180)
traffic_light2 = TrafficLight(position=(-71.90, -3.75, 75.00), rotation_y=90)
traffic_light3 = TrafficLight(position=(-71.90, -3.75, 55.50), rotation_y=270)

traffic_light4 = TrafficLight(position=(-71.90, -3.75, 192.50), rotation_y=0)
traffic_light5 = TrafficLight(position=(-52.40, -3.75, 202.15), rotation_y=90)
traffic_light6 = TrafficLight(position=(-52.40, -3.75, 182.80), rotation_y=270)

traffic_light7 = TrafficLight(position=(-52.40, -3.75, -62.30), rotation_y=180)
traffic_light8 = TrafficLight(position=(-71.90, -3.75, -72.10), rotation_y=270)
traffic_light9 = TrafficLight(position=(-71.90, -3.75, -52.50), rotation_y=90)

traffic_light10 = TrafficLight(position=(-71.90, -3.75, -190.80), rotation_y=0)
traffic_light11 = TrafficLight(position=(-52.40, -3.75, -200.65), rotation_y=270)
traffic_light12 = TrafficLight(position=(-52.40, -3.75, -181.00), rotation_y=90)

traffic_light13 = TrafficLight(position=(-198.60, -3.75, -301.35), rotation_y=0)
traffic_light14 = TrafficLight(position=(-198.60, -3.75, -320.75), rotation_y=270)
traffic_light15 = TrafficLight(position=(-179.15, -3.75, -320.75), rotation_y=180)
traffic_light16 = TrafficLight(position=(-179.15, -3.75, -301.35), rotation_y=90)

traffic_light17 = TrafficLight(position=(-198.40, -3.75, -52.55), rotation_y=0)
traffic_light18 = TrafficLight(position=(-198.40, -3.75, -72.07), rotation_y=270)
traffic_light19 = TrafficLight(position=(-178.98, -3.75, -72.07), rotation_y=180)
traffic_light20 = TrafficLight(position=(-178.98, -3.75, -52.55), rotation_y=90)

traffic_light21 = TrafficLight(position=(-198.45, -3.75, 74.80), rotation_y=0)
traffic_light22 = TrafficLight(position=(-198.45, -3.75, 55.39), rotation_y=270)
traffic_light23 = TrafficLight(position=(-179.05, -3.75, 55.39), rotation_y=180)
traffic_light24 = TrafficLight(position=(-179.05, -3.75, 74.80), rotation_y=90)

traffic_light25 = TrafficLight(position=(-198.45, -3.75, 326.45), rotation_y=0)
traffic_light26 = TrafficLight(position=(-198.45, -3.75, 306.92), rotation_y=270)
traffic_light27 = TrafficLight(position=(-178.90, -3.75, 306.92), rotation_y=180)
traffic_light28 = TrafficLight(position=(-178.90, -3.75, 326.45), rotation_y=90)

traffic_light29 = TrafficLight(position=(-305.82, -3.75, 192.35), rotation_y=180)
traffic_light30 = TrafficLight(position=(-325.33, -3.75, 202.30), rotation_y=90)
traffic_light31 = TrafficLight(position=(-325.33, -3.75, 182.65), rotation_y=270)

traffic_light32 = TrafficLight(position=(-325.33, -3.75, 65.10), rotation_y=0)
traffic_light33 = TrafficLight(position=(-305.82, -3.75, 74.75), rotation_y=90)
traffic_light34 = TrafficLight(position=(-305.82, -3.75, 55.30), rotation_y=270)

traffic_light35 = TrafficLight(position=(-325.33, -3.75, -62.45), rotation_y=0)
traffic_light36 = TrafficLight(position=(-305.82, -3.75, -52.70), rotation_y=90)
traffic_light37 = TrafficLight(position=(-305.82, -3.75, -72.10), rotation_y=270)

traffic_light38 = TrafficLight(position=(-305.82, -3.75, -190.80), rotation_y=180)
traffic_light39 = TrafficLight(position=(-325.33, -3.75, -181.20), rotation_y=90)
traffic_light40 = TrafficLight(position=(-325.33, -3.75, -200.60), rotation_y=270)


def update():
    # Update traffic light state
    if traffic_light1:
        traffic_light1.update()
        traffic_light2.update()
        traffic_light3.update()


def input(key):
    # If left-clicked, show the player's coordinates
    if held_keys['left mouse']:
        print_cords()

    # If right-clicked, switch traffic light to green
    if held_keys['right mouse']:
        traffic_light1.switch_to_green()
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
