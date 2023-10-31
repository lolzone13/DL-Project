from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController

window.title = "engine"

def make_walls(grid, scale=(10, 50, 10)):
	number_of_walls = 100

	walls = [None]*number_of_walls

	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j]:
				walls[i*10 + j] = Entity(model="cube", collider="box", position=(20*i - 100, 0, 20*j - 100), scale=scale, rotation=(0,0,0),
								texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))


class Human(Button):
	def __init__(self, x, y, z):
		super().__init__(
			parent=scene,
			model="assets/person_tom_1.obj",
			scale=1,
			position=(x,y,z),
			rotation=(0, 90, 0),
			collider="box"
		)

def input(key):
	if key == "w":
		print(player.position)
		direction = Vec3(
            player.forward * (held_keys['w'] - held_keys['s'])
            + player.right * (held_keys['d'] - held_keys['a'])
            ).normalized()  
		hit_info = boxcast(player.position, thickness=(3,3), direction=direction, debug=False)
		print(hit_info.distance)



app = Ursina(size=(640,640), borderless=False, vsync=False)
Sky()
player = FirstPersonController(y=5, origin_y=-.5, gravity=0)
ground = Entity(model='plane', scale=(170, 1, 170), color=color.lime, texture="white_cube",
				texture_scale=(100, 100), collider='box')

grid = [
	[0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
	[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
	[0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]

# walls, create them programmatically based on grid
make_walls(grid)


num = 100
humans=[None]*num
for i in range(num):
	sx=uniform(-50, 50)
	sy=uniform(-50, 50)
	sz=uniform(-50, 50)
	humans[i]=Human(sx, 0, sz)

app.run()