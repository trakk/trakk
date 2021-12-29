class Task():
	_defs = [
		("task_id", ""),
		("category_id", None),
		("task_title", ""),
		("task_description", ""),
		("task_status", "open")
	]
	_attr = [d[0] for d in _defs]

	def __init__(self, data=None):
		if data is None:
			data = {}
		self.merge(data)


	def merge(self, data=None):
		if data is None:
			data = {}
		for field, default, *_type in Task._defs:
			if _type:
				value = _type[0](data[field]) if field in data else default
			else:
				value = data[field] if field in data else default
			setattr(self, field, value)


	def asdict(self):
		d = {}
		for field in Task._attr:
			value = getattr(self, field)
			if hasattr(value, "asdict") and callable(value.asdict):
				value = value.asdict()
			d[field] = value
		return d


	def fetch(self, db):
		q = """
			SELECT
				*
			FROM tasks t
			WHERE 1=1
				AND t.task_id = %s
		"""
		ps = (self.task_id,)
		row = db.find_one(q, ps)
		self.merge(row)


	@staticmethod
	def fetch_by_id(task_id, db):
		t = Task(dict(task_id=task_id))
		t.fetch(db)
		return t


	def insert(self, db):
		q = """
			INSERT INTO tasks (category_id, task_title, task_description, task_status)
			VALUES
			(%s, %s, %s, %s)
			RETURNING task_id
		"""
		ps = (self.category_id, self.task_title, self.task_description, self.task_status)
		row = db.find_one(q, ps)
		self.task_id = row["task_id"]


	def update(self, db):
		q = """
			INSERT INTO tasks (task_id, category_id, task_title, task_description, task_status)
			VALUES
			(%s, %s, %s, %s, %s)
			ON CONFLICT (task_id)
			DO UPDATE SET
				category_id=EXCLUDED.category_id,
				task_title=EXCLUDED.task_title,
				task_description=EXCLUDED.task_description,
				task_status=EXCLUDED.task_status
		"""
		ps = (self.task_id, self.category_id, self.task_title, self.task_description, self.task_status)
		db.do(q, ps)






