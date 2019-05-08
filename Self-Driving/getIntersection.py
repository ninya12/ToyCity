class Point(object):
	"""docstring for Point"""
	def __init__(self, x, y):
		super(Point, self).__init__()
		self.x = float(x)
		self.y = float(y)


def getIntersection(x1, x2, x3, x4):
	parallel1 = (x1.x == x2.x)
	parallel2 = (x3.x == x4.x)
	result = Point(-1, -1)

	if(parallel1):
		sameValue1 = x1.x
	else:
		increase1 = (x2.y - x1.y)/(x2.x - x1.x)
		constant1 = x1.y - increase1 * x1.x

	if(parallel2):
		sameValue2 = x3.x
	else:
		increase2 = (x4.y - x3.y)/(x4.x - x3.x)
		constant2 = x3.y - increase2 * x3.x	

	if(parallel1 and parallel2):
		return result
	if(parallel1):
		result = Point(sameValue1, increase2 * sameValue1 + constant2)
	elif(parallel2):
		result = Point(sameValue2, increase1 * sameValue2 + constant1)
	else:
		result.x = -(constant1 - constant2)/(increase1- increase2)
		result.y = increase1 * result.x + constant1
	return result
  
