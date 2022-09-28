import pygame
import os
import csv
from spritesheet import Spritesheet
from color import Color

class Object:
	def __init__(self, x, y, x_size, y_size, color = Color.green):
		self.x = x
		self.y = y
		self.x_size = x_size
		self.y_size = y_size
		self.color = color

	def draw(self, screen, camera):
		pygame.draw.rect(screen, self.color, (self.x - camera.x, self.y - camera.y, self.x_size, self.y_size))

class BG_Image:
	def __init__(self, filename, distance, map, screen):  # Set distance to 1 for a close up background image
		self.image = pygame.image.load(filename).convert_alpha()
		self.x_offset = 0
		self.y_offset = 0
		rect = self.image.get_rect()
		width = screen.width + (map.width - screen.width) / distance
		height = screen.height + (map.height - screen.height) / distance

		horizontal_ratio = width / rect[2]
		vertical_ratio = height / rect[3]
		if horizontal_ratio > vertical_ratio:
			self.y_offset -= (int(rect[3] * horizontal_ratio) - height) / 2
			height = int(rect[3] * horizontal_ratio)
		if horizontal_ratio < vertical_ratio:
			self.x_offset -= (int(rect[2] * vertical_ratio) - width) / 2
			width = int(rect[2] * vertical_ratio)

		self.image = pygame.transform.scale(self.image, (width, height))
		self.distance = distance

	def draw (self, screen, camera):
		screen.blit(self.image, (self.x_offset - camera.x / self.distance, self.y_offset - camera.y / self.distance))

class TileMap():
	def __init__(self, spritesheet,
		csv_behind_player,
		csv_before_player,
		csv_hitbox,
		PlayerXStartingPosition, PlayerYStartingPosition, colorkey = (0,0,0)):

		self.cell_width = spritesheet.cell_width
		self.cell_height = spritesheet.cell_height

		self.csv_behind_player = csv_behind_player
		self.csv_before_player = csv_before_player
		self.csv_hitbox = csv_hitbox

		self.behind_player_map = self.read_csv(self.csv_behind_player)
		self.before_player_map = self.read_csv(self.csv_before_player)
		self.hitbox_map = self.read_csv(self.csv_hitbox)

		self.BG_images = []

		self.rows = len(self.hitbox_map)
		self.columns = len(self.hitbox_map[0])
		self.width = self.cell_width * self.columns
		self.height = self.cell_height * self.rows

		self.colorkey = colorkey
		self.BG_objects = []
		self.BG_objects.append(Object(-1, -1, 0, self.height + 2))
		self.BG_objects.append(Object(-1, -1, self.width + 2, 0))
		self.BG_objects.append(Object(-1, self.height + 1, self.width + 2, 0))
		self.BG_objects.append(Object(self.width + 1, -1, 0, self.height + 2))

		self.image_behind_player = pygame.Surface((self.width, self.height)).convert()
		self.image_before_player = pygame.Surface((self.width, self.height)).convert()

		for y in range(self.rows):
			for x in range(self.columns):
				tile_behind_player = int(self.behind_player_map[y][x])
				tile_before_player = int(self.before_player_map[y][x])
				tile_hitbox = int(self.hitbox_map[y][x])

				if tile_behind_player != -1:
					self.image_behind_player.blit(spritesheet.images[tile_behind_player], (x * self.cell_width, y * self.cell_height))

				if tile_before_player != -1:
					self.image_before_player.blit(spritesheet.images[tile_before_player], (x * self.cell_width, y * self.cell_height))

				if tile_hitbox != -1:
					self.BG_objects.append(Object(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height))

		self.image_behind_player.set_colorkey(self.colorkey)
		self.image_before_player.set_colorkey(self.colorkey)

		self.player_x_starting_position = PlayerXStartingPosition
		self.player_y_starting_position = PlayerYStartingPosition

	def read_csv(self, csv_filename):
		map = []
		with open(os.path.join(csv_filename)) as data:
			data = csv.reader(data, delimiter = ",")
			for row in data:
				map.append(list(row))
		return map

	def draw_before_player(self, screen, camera):
		screen.blit(self.image_before_player, (- camera.x, - camera.y))

	def add_BG_images(self, list_of_filenames, list_of_distances, screen):
		for i in range(len(list_of_filenames)):
			self.BG_images.append(BG_Image(list_of_filenames[i], list_of_distances[i], self, screen))

	def draw_behind_player(self, screen, camera):
		if len(self.BG_images) > 0:
			for image in self.BG_images:
				image.draw(screen, camera)
		screen.blit(self.image_behind_player, (- camera.x, - camera.y))