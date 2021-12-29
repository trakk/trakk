import time

import psycopg2
import psycopg2.extras


# fairly robust/complete looking retry/reconnect gist
# https://gist.github.com/cabecada/da8913830960a644755b18a02b65e184


class Db:
	def __init__(self, config):
		self.config = config
		self.connect()
		self.cursor()


	def connect(self):
		self.conn = psycopg2.connect(
			database=self.config["name"],
			user=self.config["user"],
			password=self.config["pass"],
			host=self.config["host"])
		self.conn.set_client_encoding("UTF8")
		return self.conn


	def cursor(self):
		self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		return self.cur


	def do(self, query, params=(), num_tries=2):
		errors = []
		for i in range(0, num_tries):
			try:
				self.cur.execute(query, params)
				self.conn.commit()
				break
			except psycopg2.OperationalError as e:
				print(f"Query attempt #{i}/{num_tries} failed")
				errors.append(e)
				time.sleep(1)
				self.connect()
				self.cursor()
		if errors:
			print(errors)


	def find(self, query, params=(), num_tries=2):
		errors = []
		rows = None
		for i in range(0, num_tries):
			try:
				self.cur.execute(query, params)
				rows = self.cur.fetchall()
				self.conn.commit()
				break
			except psycopg2.OperationalError as e:
				print(f"Query attempt #{i}/{num_tries} failed")
				errors.append(e)
				time.sleep(1)
				self.connect()
				self.cursor()
		if errors:
			print(errors)
		return rows


	def find_one(self, query, params=(), num_tries=2):
		errors = []
		row = None
		for i in range(0, num_tries):
			try:
				self.cur.execute(query, params)
				row = self.cur.fetchone()
				self.conn.commit()
				break
			except psycopg2.OperationalError as e:
				print(f"Query attempt #{i}/{num_tries} failed")
				errors.append(e)
				time.sleep(1)
				self.connect()
				self.cursor()
		if errors:
			print(errors)
		return row

