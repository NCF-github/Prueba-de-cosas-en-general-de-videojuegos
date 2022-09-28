import pygame

# Aviable modes:
#
# FollowPlayer
# FollowPlayerHorizontaly
# FollowPlayerVerticaly
#
# FollowPlayerWithBorders
# FollowPlayerHorizontalyWithBorders
# FollowPlayerVerticalyWithBorders
#
# Auto  (set speed on an axis to 0 to get a 1 axis scroll)
# AutoHorizontalyFollowVerticaly
# AutoVerticalyFollowHorizontaly
#
# AutoHorizontalyFollowVerticalyWithBorders
# AutoVerticalyFollowHorizontalyWithBorders
#
# NoMovement


class Camera:
	def __init__(self, mode = "FollowPlayerWithBorders", player = "none", smoothness = 10):
		self.mode = mode
		self.x_float = player.x
		self.y_float = player.y
		self.x = player.x
		self.y = player.y
		self.smoothness = smoothness

	def define_borders(self, top_border = "none", bottom_border = "none", left_border = "none", right_border = "none"):
		self.top_border = top_border
		self.bottom_border = bottom_border
		self.right_border = right_border
		self.left_border = left_border
	def define_auto_scroll_speed(self, horizontal_scroll_speed = 1, vertical_scroll_speed = 0):
		self.horizontal_scroll_speed = horizontal_scroll_speed
		self.vertical_scroll_speed = vertical_scroll_speed

	def scroll(self, screen, player = "none"):
		if self.mode == "FollowPlayer":
			self.scroll_follow_player(screen, player)
		if self.mode == "FollowPlayerHorizontaly":
			self.scroll_follow_player_horizontaly(screen, player)
		if self.mode == "FollowPlayerVerticaly":
			self.scroll_follow_player_verticaly(screen, player)

		if self.mode == "FollowPlayerWithBorders":
			self.scroll_follow_player_with_borders(screen, player)
		if self.mode == "FollowPlayerHorizontalyWithBorders":
			self.scroll_follow_player_horizontaly_with_borders(screen, player)
		if self.mode == "FollowPlayerVerticalyWithBorders":
			self.scroll_follow_player_verticaly_with_borders(screen, player)

		if self.mode == "Auto":
			self.scroll_auto()
		if self.mode == "AutoHorizontalyFollowVerticaly":
			self.scroll_auto_horizontaly_follow_verticaly(screen, player)
		if self.mode == "AutoVerticalyFollowHorizontaly":
			self.scroll_auto_verticaly_follow_horizontaly(screen, player)

		if self.mode == "AutoHorizontalyFollowVerticalyWithBorders":
			self.scroll_auto_horizontaly_follow_verticaly_with_borders(screen, player)
		if self.mode == "AutoVerticalyFollowHorizontalyWithBorders":
			self.scroll_auto_verticaly_follow_horizontaly_with_borders(screen, player)

		if self.mode == "NoMovement":
			self.scroll_no_movement()

		self.x = int(self.x_float)
		self.y = int(self.y_float)

	def scroll_follow_player(self, screen, player):
		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2))
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness

		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness
	def scroll_follow_player_horizontaly(self, screen, player):
		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2)) 
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness
	def scroll_follow_player_verticaly(self, screen, player):
		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness

	def scroll_follow_player_with_borders(self, screen, player):
		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2))
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness

		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness

		if self.x_float + screen.width > self.right_border:
			self.x_float = self.right_border - screen.width
		if self.x_float < self.left_border:
			self.x_float = self.left_border

		if self.y_float + screen.height > self.bottom_border:
			self.y_float = self.bottom_border - screen.height
		if self.y_float < self.top_border:
			self.y_float = self.top_border
	def scroll_follow_player_horizontaly_with_borders(self, screen, player):
		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2))
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness

		if self.x_float + screen.width > self.right_border:
			self.x_float = self.right_border - screen.width
		if self.x_float < self.left_border:
			self.x_float = self.left_border
	def scroll_follow_player_verticaly_with_borders(self, screen, player):
		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness

		if self.y_float + screen.height > self.bottom_border:
			self.y_float = self.bottom_border - screen.height
		if self.y_float < self.top_border:
			self.y_float = self.top_border

	def scroll_auto(self):
		self.x_float += self.horizontal_scroll_speed
		self.y_float += self.vertical_scroll_speed
	def scroll_auto_horizontaly_follow_verticaly(self, screen, player):
		self.x_float += self.horizontal_scroll_speed

		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness
	def scroll_auto_verticaly_follow_horizontaly(self, screen, player):
		self.y_float += self.vertical_scroll_speed

		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2)) 
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness

	def scroll_auto_horizontaly_follow_verticaly_with_borders(self, screen, player):
		self.x_float += self.horizontal_scroll_speed

		if (player.y + (player.y_size / 2)) - self.y_float != screen.height / 2:
			if self.smoothness <= 0:
				self.y_float += player.y - (self.y_float + (screen.height / 2))
			else:
				self.y_float += (player.y - (self.y_float + (screen.height / 2))) / self.smoothness

		if self.y_float + screen.height > self.bottom_border:
			self.y_float = self.bottom_border - screen.height
		if self.y_float < self.top_border:
			self.y_float = self.top_border
	def scroll_auto_verticaly_follow_horizontaly_with_borders(self, screen, player):
		self.y_float += self.vertical_scroll_speed

		if (player.x + (player.x_size / 2)) - self.x_float != screen.width / 2:
			if self.smoothness <= 0:
				self.x_float += player.x - (self.x_float + (screen.width / 2)) 
			else:
				self.x_float += (player.x - (self.x_float + (screen.width / 2))) / self.smoothness

		if self.x_float + screen.width > self.right_border:
			self.x_float = self.right_border - screen.width
		if self.x_float < self.left_border:
			self.x_float = self.left_border

	def scroll_no_movement(self):
		self.x_float = 0
		self.y_float = 0