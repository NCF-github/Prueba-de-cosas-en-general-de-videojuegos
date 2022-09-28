import pygame
import random
pygame.init()


class Game:
	def __init__(self):
		self.right = False
		self.left = False
		self.space = False
		self.space_released = True
		self.game_over = False

		self.f = False
		self.f_released = False
		self.d = False
		self.s = False

	def update_key_states(self):
		self.space = False
		self.f = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game_over = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and self.space_released == True:
					self.space = True
					self.space_released = False
				if event.key == pygame.K_RIGHT:
					self.right = True
				if event.key == pygame.K_LEFT:
					self.left = True

				if event.key == pygame.K_f and self.f_released == True:
					self.f = True
					self.f_released = False
				if event.key == pygame.K_d:
					self.d = True
				if event.key == pygame.K_s:
					self.s = True


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.space_released = True
				if event.key == pygame.K_RIGHT:
					self.right = False
				if event.key == pygame.K_LEFT:
					self.left = False

				if event.key == pygame.K_f:
					self.f_released = True
				if event.key == pygame.K_d:
					self.d = False
				if event.key == pygame.K_s:
					self.s = False