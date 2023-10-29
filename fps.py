from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController


def make_walls(grid, scale=(8, 5, 8)):
	number_of_walls = 100

	walls = [None]*number_of_walls

	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j]:
				walls[i*10 + j] = Entity(model="cube", collider="box", position=(20*i - 100, 0, 20*j - 100), scale=scale, rotation=(0,0,0),
								texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))




def input(key):
	# if key=="left mouse down":
	# 	Audio("assets/laser_sound.wav")
	# 	Animation("assets/spark", parent=camera.ui, fps=5, scale=.1, position=(.19, -.03), loop=False)

	# 	# for wasp in wasps:
	# 	# 	if wasp.hovered:
	# 	# 		destroy(wasp)
	# 	for spider in spiders:
	# 		if spider.hovered:
	# 			destroy(spider)

	pass

class Wasp(Button):
	def __init__(self, x, y, z):
		super().__init__(
			parent=scene,
			model="assets/wasp.obj",
			scale=.1,
			position=(x,y,z),
			rotation=(0, 90, 0),
			collider="box"
			)

class Spider(Button):
	def __init__(self, x, y, z):
		super().__init__(
			parent=scene,
			model="assets/spider.obj",
			scale=.02,
			position=(x,y,z),
			rotation=(0, 90, 0),
			collider="box"
			)

app=Ursina(fullscreen=True)

Sky()
player=FirstPersonController(y=2, origin_y=-.5, speed=8)
ground=Entity(model='plane', scale=170, color=color.lime, texture="white_cube",
	texture_scale=(100, 100), collider='box')



grid = [
	[0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
	[0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
	[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
	[0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]



# walls, create them programmatically based on grid


make_walls(grid)

map_origin=Entity(model="cube", collider="box", position=(0, 0, 0), scale=(1, 5, 1), rotation=(0,0,0),
	texture="white_cube", texture_scale=(5,5), color=color.rgb(255, 128, 0))
# wall_1=Entity(model="cube", collider="box", position=(-8, 0, 0), scale=(3, 5, 3), rotation=(0,0,0),
# 	texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))
# wall_2 = duplicate(wall_1, z=20)
# wall_3=duplicate(wall_1, z=10)
# wall_4=Entity(model="cube", collider="box", position=(-15, 0, 10), scale=(3, 5, 3), rotation=(0,0,0),
# 	texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))

# gun=Entity(model="assets/gun.obj", parent=camera.ui, scale=.08, color=color.gold, position=(.3, -.2),
# 	rotation=(-5, -10, -10))

num=10
wasps=[None]*num
spiders=[None]*num
for i in range(num):
	# wx=uniform(-12, -7)
	# wy=uniform(.1, 1.8)
	# wz=uniform(.8, 3.8)
	# wasps[i]=Wasp(wx, wy, wz)
	# wasps[i].animate_x(wx+.5, duration=.2, loop=True)

	sx=uniform(-100, 100)
	sy=uniform(-100, 100)
	sz=uniform(-100, 100)
	spiders[i]=Spider(sx, 2, sz)
	# spiders[i].animate_x(sx+.5, duration=.2, loop=True)

app.run()



print("hello world")


# from ursina import Ursina, Sky, load_model, color, Text, window
# app = Ursina(vsync=False)
# '''
# Simple camera for debugging.
# Hold right click and move the mouse to rotate around point.
# '''

# sky = Sky()
# e = Entity(model=load_model('cube', use_deepcopy=True), color=color.white, collider='box')
# e.model.colorize()

# from ursina.prefabs.first_person_controller import FirstPersonController

# ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=(32,32), collider='box')
# box = Entity(model='cube', collider='box', texture='white_cube', scale=(10,2,2), position=(2,1,5), color=color.light_gray)
# player = FirstPersonController(y=1, enabled=True)

# ec = EditorCamera()
# ec.enabled = False
# rotation_info = Text(position=window.top_left)




# def update():
#     rotation_info.text = str(int(ec.rotation_y)) + '\n' + str(int(ec.rotation_x))


# def input(key):
#     if key == 'tab':    # press tab to toggle edit/play mode
#         ec.enabled = not ec.enabled
#     elif key == 'space':
#         mouse.locked = True
#         print(mouse.velocity)
# app.run()


