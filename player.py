from color import Color
from spritesheet import Spritesheet, Animation
import pygame
import math
import random
pygame.init()

class Player:
	def __init__(self, x=0, y=0, x_size=50, y_size=80, gravity_acceleration=1.4, max_horizontal_speed=15, horizontal_acceleration=2.5, horizontal_desacceleration=2,
		horizontal_in_animation_desacceleration = 0.4, frame_speed = 5, jump_power=25, jumps=2, jump_limit=True, walljump=True, walljump_repulsion_power=10,
		color=Color.red, wall_slide=True, wall_slide_speed=5, hitbox=False, coyote_frames = 3, scale = 3):
		self.x = x
		self.y = y
		self.x_size = x_size
		self.y_size = y_size
		self.X_center = self.x + (self.x_size / 2)
		self.y_center = self.y + (self.y_size / 2)
		self.gravity_acceleration = gravity_acceleration
		self.max_horizontal_speed = max_horizontal_speed
		self.horizontal_acceleration = horizontal_acceleration
		self.horizontal_desacceleration = horizontal_desacceleration
		self.horizontal_in_animation_desacceleration = horizontal_in_animation_desacceleration
		self.jump_power = jump_power
		self.jumps = jumps
		self.jump_limit = jump_limit
		self.walljump = walljump
		self.walljump_repulsion_power = walljump_repulsion_power
		self.color = color
		self.wall_slide = wall_slide
		self.wall_slide_speed = wall_slide_speed
		self.wallcling = False
		self.hitbox = hitbox
		if self.jump_limit == False and self.jumps <= 1:
			self.jumps = 10

		self.x_speed = 0
		self.y_speed = 0
		self.jump_count = jumps
		self.coyote_frames = coyote_frames
		self.time_since_touching_the_floor = 0
		self.time_since_touching_right_wall = 0
		self.time_since_touching_left_wall = 0

		self.k_right = False
		self.k_left = False
		self.k_space = False
		self.hurt = False

		self.colision_right = False
		self.colision_left = False
		self.colision_up = False
		self.colision_down = False

		self.scale = scale
		self.idle = Animation("folder", filename = "./assets/Warrior/IndividualSprites/idle/Warrior_Idle_", number_of_frames = 6, scale = self.scale, filetype = ".png")
		self.running = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Run/Warrior_Run_", number_of_frames = 8, scale = self.scale, filetype = ".png")
		self.death = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Death-Effect/Warrior_Death_", number_of_frames = 11, scale = self.scale, filetype = ".png")
		self.wall_sliding = Animation("folder", filename = "./assets/Warrior/IndividualSprites/WallSlide/Warrior_WallSlide_", number_of_frames = 3, scale = self.scale, filetype = ".png")
		self.rising = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Jump/Warrior_Jump_", number_of_frames = 3, scale = self.scale, filetype = ".png")
		self.rising_to_falling = Animation("folder", filename = "./assets/Warrior/IndividualSprites/UptoFall/Warrior_Uptofall_", number_of_frames = 2, scale = self.scale, filetype = ".png")
		self.falling = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Fall/Warrior_Fall_", number_of_frames = 3, scale = self.scale, filetype = ".png")
		self.hurting = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Hurt-Effect/Warrior_hurt_", number_of_frames = 4, scale = self.scale, filetype = ".png")
		self.attacking_no_sword = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Attack/Warrior_Attack-NoSword_", number_of_frames = 12, scale = self.scale, filetype = ".png")
		self.attacking_with_sword = Animation("folder", filename = "./assets/Warrior/IndividualSprites/Attack/Warrior_Attack_", number_of_frames = 12, scale = self.scale, filetype = ".png")

		self.direction = "right"
		self.current_animation = self.idle.flipped_frames
		self.current_frame = self.current_animation[0]
		self.in_animation = False
		self.hurtrames_still_left = 0
		self.a = 0
		self.b = -1
		self.frame_speed = frame_speed

		self.second_attack = False

	def draw(self, screen, camera):
		if self.hitbox == True:
			pygame.draw.rect(screen, self.color, (self.x - camera.x, self.y - camera.y, self.x_size, self.y_size))

		if self.a % self.frame_speed == 0:
			self.b += 1
		self.a += 1
		self.current_frame = self.current_animation[self.b % len(self.current_animation)]
		screen.blit(self.current_frame, (self.x - camera.x, self.y - camera.y))

		if self.current_animation == self.attacking_no_sword.frames:
			idx = self.b % len(self.current_animation)
			screen.blit(self.attacking_with_sword.frames[idx], ((self.x - 9 * self.scale) - camera.x, (self.y - 10 * self.scale) - camera.y))
		if self.current_animation == self.attacking_no_sword.flipped_frames:
			idx = self.b % len(self.current_animation)
			screen.blit(self.attacking_with_sword.flipped_frames[idx], ((self.x - 20 * self.scale) - camera.x, (self.y - 10 * self.scale) - camera.y))

	def get_inputs(self, game):
			self.k_right = game.right
			self.k_left = game.left
			self.k_space = game.space
			self.k_attack = game.f
			self.hurt_from_right = game.d
			self.hurt_from_left = game.s
			self.hurt = False
			if self.hurt_from_left == True or self.hurt_from_right == True:
				self.hurt = True
			if self.k_right == True and self.k_left == True:
				self.k_right = False
				self.k_left = False

	def update_speed(self, BG_objects):
		if not self.wallcling:
			self.y_speed += self.gravity_acceleration

		if not self.in_animation or self.current_animation == self.rising_to_falling.frames or self.current_animation == self.rising_to_falling.flipped_frames:
			if self.k_right == True:
				self.x_speed += self.horizontal_acceleration
			if self.k_left == True:
				self.x_speed -= self.horizontal_acceleration

		if (self.k_right == False and self.k_left == False) or (self.in_animation and self.current_animation != self.rising_to_falling.frames and self.current_animation != self.rising_to_falling.flipped_frames):
			desacceleration = self.horizontal_desacceleration
			if self.in_animation and self.current_animation != self.rising_to_falling.frames and self.current_animation != self.rising_to_falling.flipped_frames:
				desacceleration = self.horizontal_in_animation_desacceleration
				self.update_state(BG_objects)
				if self.colision_down == True:
					desacceleration *= 3

			if self.x_speed > 0:
				if self.x_speed < desacceleration:
					self.x_speed = 0
				else:
					self.x_speed -= desacceleration
			elif self.x_speed < 0:
				if self.x_speed > -desacceleration:
					self.x_speed = 0
				else:
					self.x_speed += desacceleration
		
		if self.x_speed > self.max_horizontal_speed:
			self.x_speed = self.max_horizontal_speed
		if self.x_speed < -self.max_horizontal_speed:
			self.x_speed = -self.max_horizontal_speed

		if self.hurt == True:
			self.y_speed = -5
			if self.hurt_from_left:
				self.x_speed = 7
			elif self.hurt_from_right:
				self.x_speed = -7
	def update_speed_after_colision(self):
		if self.x_speed > 0 and self.colision_right == True:
			self.x_speed = 0
		if self.x_speed < 0 and self.colision_left == True:
			self.x_speed = 0
		if self.y_speed > 0 and self.colision_down == True:
			self.y_speed = 0
		if self.y_speed < 0 and self.colision_up == True:
			self.y_speed = 0

		self.wallcling = False
		if self.wall_slide == True:
			if self.y_speed >= 0:
				if self.colision_down == False:
					if self.colision_right == True or self.colision_left == True:
						self.y_speed = self.wall_slide_speed
						self.wallcling = True

	def jump(self):
		if self.k_space == True:
			self.cancel_animations([self.rising_to_falling.frames, self.rising_to_falling.flipped_frames])
			if not self.in_animation:
				if self.jumps == 1:
					if self.k_space == True:
						if self.walljump == True:
							if self.colision_down == False:
								if self.colision_left == True:
									self.y_speed = -self.jump_power
									self.x_speed = self.walljump_repulsion_power
								if self.colision_right == True:
									self.y_speed = -self.jump_power
									self.x_speed = -self.walljump_repulsion_power
						if self.colision_down == True:
							self.y_speed = -self.jump_power
				else:
					if self.k_space == True:
						if self.walljump == True:
							if self.colision_down == False:
								if self.time_since_touching_left_wall <= self.coyote_frames:
									self.x_speed = self.walljump_repulsion_power
									self.jump_count += 1
								if self.time_since_touching_right_wall <= self.coyote_frames:
									self.x_speed = -self.walljump_repulsion_power
									self.jump_count += 1
						if self.jump_count > 0:
							self.y_speed = -self.jump_power
							if self.jump_limit == True:
								self.jump_count -= 1
	def recharge_jumps(self):
		if self.time_since_touching_the_floor <= self.coyote_frames:
			self.jump_count = self.jumps - 1

		if self.colision_down == True:
			self.time_since_touching_the_floor = 0
		else:
			self.time_since_touching_the_floor += 1

		if self.colision_right == True:
			self.time_since_touching_right_wall = 0
		else:
			self.time_since_touching_right_wall += 1

		if self.colision_left == True:
			self.time_since_touching_left_wall = 0
		else:
			self.time_since_touching_left_wall += 1

	def detect_colision_right(self, BG_objects):
		self.colision_right = False	
		for object in BG_objects:
			if int(self.x) == object.x - self.x_size:
				if int(self.y) > object.y - self.y_size and int(self.y) < object.y + object.y_size:
					self.colision_right = True
	def detect_colision_left(self, BG_objects):
		self.colision_left = False
		for object in BG_objects:
			if int(self.x) == object.x + object.x_size:
				if int(self.y) > object.y - self.y_size and int(self.y) < object.y + object.y_size:
					self.colision_left = True
	def detect_colision_down(self, BG_objects):
		self.colision_down = False
		for object in BG_objects:
			if int(self.y) == object.y - self.y_size:
				if int(self.x) > object.x - self.x_size and int(self.x) < object.x + object.x_size:
					self.colision_down = True
	def detect_colision_up(self, BG_objects):
		self.colision_up = False
		for object in BG_objects:
			if int(self.y) == object.y + object.y_size:
				if int(self.x) > object.x - self.x_size and int(self.x) < object.x + object.x_size:
					self.colision_up = True

	def update_state(self, BG_objects):
		self.colision_up = False
		self.colision_down = False
		self.colision_left = False
		self.colision_right = False
		self.detect_colision_up(BG_objects)
		self.detect_colision_down(BG_objects)
		self.detect_colision_left(BG_objects)
		self.detect_colision_right(BG_objects)

	def move_right(self, BG_objects):
		if self.x_speed > 0:
			for i in range(int(self.x_speed)):
				self.detect_colision_right(BG_objects)
				if not self.colision_right:
					self.x += 1
	def move_left(self, BG_objects):
		if self.x_speed < 0:
			for i in range(-int(self.x_speed)):
				self.detect_colision_left(BG_objects)
				if not self.colision_left:
					self.x -= 1
	def move_down(self, BG_objects):
		if self.y_speed > 0:
			for i in range(int(self.y_speed)):
				self.detect_colision_down(BG_objects)
				if not self.colision_down:
					self.y += 1
	def move_up(self, BG_objects):
		if self.y_speed < 0:
			for i in range(-int(self.y_speed)):
				self.detect_colision_up(BG_objects)
				if not self.colision_up:
					self.y -= 1

	def move(self, map):
		self.move_right(map.BG_objects)
		self.move_left(map.BG_objects)
		self.move_down(map.BG_objects)
		self.move_up(map.BG_objects)

		if self.x < 0:
			self.x = 0
		if self.x + self.x_size > map.width:
			self.x = map.width - self.x_size
		if self.y < 0:
			self.y = 0
		if self.y + self.y_size > map.height:
			self.y = map.height - self.y_size

		self.update_state(map.BG_objects)

	def get_distance_from_object_right(self, x, y, x_size, y_size, BG_objects):
		x = int(x)
		y = int(y)
		distance_right = BG_objects[0].x - (int(x) + x_size)
		distance = 0
		for object in BG_objects:
			if int(y) > object.y - y_size and int(y) < object.y + object.y_size:
				distance = object.x - (int(x) + x_size)
				if (distance < distance_right and distance >= 0) or distance_right < 0:
					distance_right = distance
		return distance_right
	def get_distance_from_object_left(self, x, y, x_size, y_size, BG_objects):
		x = int(x)
		y = int(y)
		distance_left = x - (BG_objects[0].x + BG_objects[0].x_size)
		distance = 0
		for object in BG_objects:
			if int(y) > object.y - y_size and int(y) < object.y + object.y_size:
				distance = x - (object.x + object.x_size)
				if (distance < distance_left and distance >= 0) or distance_left < 0:
					distance_left = distance
		return distance_left
	def get_distance_from_object_down(self, x, y, x_size, y_size, BG_objects):
		x = int(x)
		y = int(y)
		distance_down = BG_objects[0].y - (int(y) + y_size)
		distance = 0
		for object in BG_objects:
			if int(x) > object.x - x_size and int(x) < object.x + object.x_size:
				distance = object.y - (int(y) + y_size)
				if (distance < distance_down and distance >= 0) or distance_down < 0:
					distance_down = distance
		return distance_down
	def get_distance_from_object_up(self, x, y, x_size, y_size, BG_objects):
		x = int(x)
		y = int(y)
		distance_up = y - (BG_objects[0].y + BG_objects[0].y_size)
		distance = 0
		for object in BG_objects:
			if int(x) > object.x - x_size and int(x) < object.x + object.x_size:
				distance = y - (object.y + object.y_size)
				if (distance < distance_up and distance >= 0) or distance_up < 0:
					distance_up = distance
		return distance_up

	def change_size_old_version(self):  # Not in use
		old_x_size = self.x_size
		old_y_size = self.y_size
		new_x_size = self.current_frame.get_rect()[2]
		new_y_size = self.current_frame.get_rect()[3]

		if old_y_size != new_y_size or old_x_size != new_x_size:
			self.y -= (new_y_size - old_y_size)

			if self.colision_left == False and self.colision_right == False:
				self.x -= (new_x_size - old_x_size) / 2
			elif self.colision_right == True:
				self.x -= (new_x_size - old_x_size)
			elif self.colision_left == True:
				self.x -= 0

			self.x_size = new_x_size
			self.y_size = new_y_size
	def change_size(self, BG_objects):
		old_x_size = self.x_size
		old_y_size = self.y_size
		new_x_size = self.current_frame.get_rect()[2]
		new_y_size = self.current_frame.get_rect()[3]

		distance_left_up = self.get_distance_from_object_up(self.x, self.y, self.x_size, self.y_size, BG_objects)
		distance_left_down = self.get_distance_from_object_down(self.x, self.y, self.x_size, self.y_size, BG_objects)
		distance_left_right = self.get_distance_from_object_right(self.x, self.y, self.x_size, self.y_size, BG_objects)
		distance_left_left = self.get_distance_from_object_left(self.x, self.y, self.x_size, self.y_size, BG_objects)

		if new_y_size - old_y_size <= distance_left_up:
			self.y -= new_y_size - old_y_size
		elif new_y_size - old_y_size <= distance_left_up + distance_left_down:
			self.y -= distance_left_up
		else:
			self.y += distance_left_down
			self.y -= new_y_size - old_y_size


		if self.colision_right == True and self.colision_left == True:
			self.x -= (new_x_size - old_x_size) / 2
		elif self.colision_left == True:
			pass
		elif self.colision_right == True:
			self.x -= (new_x_size - old_x_size)

		elif distance_left_left >= (new_x_size - old_x_size) / 2 and distance_left_right >= (new_x_size - old_x_size) / 2:
			self.x -= (new_x_size - old_x_size) / 2
		elif distance_left_left < (new_x_size - old_x_size) / 2 and distance_left_right < (new_x_size - old_x_size) / 2:
			self.x -= (new_x_size - old_x_size) / 2
		elif distance_left_left < (new_x_size - old_x_size) / 2:
			self.x -= distance_left_left
		elif distance_left_right < (new_x_size - old_x_size) / 2:
			self.x += distance_left_right
			self.x -= (new_x_size - old_x_size)

		self.x_size = new_x_size
		self.y_size = new_y_size

	def enter_animation(self, animation):
		self.current_animation = animation.frames
		self.in_animation = True
		self.hurtrames_of_animation = animation.number_of_frames
		self.a = 0
		self.b = -1
	def enter_flipped_animation(self, animation):
		self.current_animation = animation.flipped_frames
		self.in_animation = True
		self.hurtrames_of_animation = animation.number_of_frames
		self.a = 0
		self.b = -1

	def cancel_animations(self, animations):   #animations must be a list of lists of frames (not an Animation object)
		for animation in animations:
			if self.current_animation == animation:
				self.in_animation = False

	def determinate_current_animation(self):
		if self.current_animation != self.hurting.frames and self.current_animation != self.hurting.flipped_frames and self.hurt == False:
			if self.x_speed > 0:
				self.direction = "right"
			if self.x_speed < 0:
				self.direction = "left"

		if not self.in_animation:
			if self.colision_down == True:
				if self.x_speed == 0 and self.k_left == False and self.k_right == False:
					if self.direction == "right":
						self.current_animation = self.idle.frames
					elif self.direction == "left":
						self.current_animation = self.idle.flipped_frames
				elif self.x_speed > 0 or self.k_right == True:
					self.current_animation = self.running.frames
				elif self.x_speed < 0 or self.k_left == True:
					self.current_animation = self.running.flipped_frames
			if self.colision_down == False:
				if self.colision_right == True:
					self.current_animation = self.wall_sliding.frames
				elif self.colision_left == True:
					self.current_animation = self.wall_sliding.flipped_frames
				elif self.y_speed < 0:
					if self.direction == "right":
						self.current_animation = self.rising.frames
					elif self.direction == "left":
						self.current_animation = self.rising.flipped_frames
				elif self.y_speed > 0:
					if self.direction == "right":
						if self.current_animation == self.rising.frames:
							self.enter_animation(self.rising_to_falling)
						else:
							self.current_animation = self.falling.frames
					elif self.direction == "left":
						if self.current_animation == self.rising.flipped_frames:
							self.enter_flipped_animation(self.rising_to_falling)
						else:
							self.current_animation = self.falling.flipped_frames
		else:
			if self.b % len(self.current_animation) == len(self.current_animation) - 1 and self.a % self.frame_speed == self.frame_speed - 1:
				self.in_animation = False

		if self.current_animation == self.attacking_no_sword.frames or self.attacking_no_sword.flipped_frames:
			if self.k_attack == True:
				self.second_attack = True
			try:
				if self.current_animation.index(self.current_frame) == 8:
					if self.second_attack == False:
						self.in_animation = False
			except:
				pass

		if self.k_attack == True:
			self.cancel_animations([self.rising_to_falling.frames, self.rising_to_falling.flipped_frames])
			if self.in_animation == False:
				if self.k_right == True:
					self.enter_animation(self.attacking_no_sword)
					self.second_attack = False
				elif self.k_left == True:
					self.enter_flipped_animation(self.attacking_no_sword)
					self.second_attack = False

				elif self.direction == "right":
					self.enter_animation(self.attacking_no_sword)
					self.second_attack = False
				elif self.direction == "left":
					self.enter_flipped_animation(self.attacking_no_sword)
					self.second_attack = False

		if self.hurt == True:
			self.cancel_animations([self.rising_to_falling.frames, self.rising_to_falling.flipped_frames, self.attacking_no_sword.frames, self.attacking_no_sword.flipped_frames])
			if self.in_animation == False:
				if self.direction == "right":
					self.enter_animation(self.hurting)
				elif self.direction == "left":
					self.enter_flipped_animation(self.hurting)


class PlayerNoAcceleration(Player):
	def update_speed(self):
		self.y_speed += self.gravity_acceleration

		if self.k_right == True:
			self.x_speed = self.max_horizontal_speed
		if self.k_left == True:
			self.x_speed = -self.max_horizontal_speed
		if self.k_right == False and self.k_left == False:
			self.x_speed = 0
		
		if self.x_speed > 0 and self.colision_right == True:
			self.x_speed = 0
		if self.x_speed < 0 and self.colision_left == True:
			self.x_speed = 0
		if self.y_speed > 0 and self.colision_down == True:
			self.y_speed = 0
		if self.y_speed < 0 and self.colision_up == True:
			self.y_speed = 0