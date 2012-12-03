

class LexicalScope (object):
	def __init__(self):
		self.bindings = {} 

	def bind(self, name, obj):
		self.bindings[name] = obj

	def unbind(self, name):
		try:
			del self.bindings[name]
			return True 
		except KeyError:
			return False 

	def query(self, name):
		try: 
			return (True, self.bindings[name])
		except KeyError:
			return (False, None)
	