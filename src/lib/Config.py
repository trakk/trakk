import os

class Config:
	def __init__(self):
		self.environment = os.getenv("TRAKK_ENV_NAME")
		self.db = {
			"name": os.getenv("DB_NAME"),
			"user": os.getenv("DB_USER"),
			"pass": os.getenv("DB_PASS"),
			"host": os.getenv("DB_HOST"),
		}

