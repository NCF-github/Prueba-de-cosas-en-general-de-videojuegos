from color import Color
from player import Player
import pygame
pygame.init()

class Screen:
	def __init__(self, width = 1400, height = 800, BG_color = Color.dark_gray, clock_tick = 60):
		self.width = width
		self.height = height
		self.BG_color = BG_color
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()
		self.clock_tick = clock_tick

	def fill_BG(self):
		self.screen.fill(self.BG_color)

	def draw_player(self, player, camera):
		player.draw(self.screen, camera)

	def update_screen(self, map, player, camera):
		self.fill_BG()
		map.draw_behind_player(self.screen, camera)

		self.draw_player(player, camera)

		map.draw_before_player(self.screen, camera)

		self.clock.tick(self.clock_tick)
		pygame.display.update()
