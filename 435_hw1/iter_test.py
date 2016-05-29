class zrange:
	def __init__(self, n):
		self.n = n

	def __iter__(self):
		return zrange_iter(self.n)
class zrange_iter:
	def __init__(self,n):
		self.i = n-1
		self.n = n
	def __iter__(self):
		return self
	def prev(self):
		if self.i >= 0:
			i = self.i
			self.i -= 1
			return i
		else:
			raise StopIteration()
