class Category():
	_defs = [
		("category_id", ""),
		("category_slug", ""),
		("category_title", ""),
		("tasks", [])
	]
	_attr = [d[0] for d in _defs]

	def __init__(self, data=None):
		if data is None:
			data = {}
		self.merge(data)


	def __repr__(self):
		return f"{self.category_slug}: {self.category_title} [{self.category_id}]"


	def __str__(self):
		return f"{self.category_title}"


	def merge(self, data=None):
		if data is None:
			data = {}
		for field, default, *_type in type(self)._defs:
			if _type:
				value = _type[0](data[field]) if field in data else default
			else:
				value = data[field] if field in data else default
			setattr(self, field, value)


	def asdict(self):
		d = {}
		for field in type(self)._attr:
			value = getattr(self, field)
			if hasattr(value, "asdict") and callable(value.asdict):
				value = value.asdict()
			d[field] = value
		return d


	def delete(self, db):
		q = """
			DELETE FROM categories WHERE category_id = %s
		"""
		ps = (self.category_id,)
		db.do(q, ps)


	def fetch(self, db):
		q = """
			SELECT
				*
			FROM categories c
			WHERE 1=1
				AND c.category_id = %s
		"""
		ps = (self.category_id,)
		row = db.find_one(q, ps)
		self.merge(row)


	@classmethod
	def fetch_by_id(class_obj, category_id, db):
		t = class_obj(dict(category_id=category_id))
		t.fetch(db)
		return t


	@classmethod
	def fetch_by_opt(class_obj, db, **kwargs):
		opt = {**kwargs}
		
		ps = []
		q = """
			SELECT
				*
			FROM categories c
			WHERE 1=1
		"""
		rows = db.find(q, ps)
		categories = [class_obj(c) for c in rows]
		return categories


	def insert(self, db):
		q = """
			INSERT INTO categories (category_slug, category_title)
			VALUES
			(%s, %s)
			RETURNING category_id
		"""
		ps = (self.category_slug, self.category_title)
		row = db.find_one(q, ps)
		self.category_id = row["category_id"]


	def update(self, db):
		q = """
			INSERT INTO categories (category_id, category_slug, category_title)
			VALUES
			(%s, %s, %s)
			ON CONFLICT (category_id)
			DO UPDATE SET
				category_slug=EXCLUDED.category_slug,
				cagegory_title=EXCLUDED.category_title
		"""
		ps = (self.category_id, self.category_slug, self.category_title)
		db.do(q, ps)






