class Point(object):
	"""docstring for Point"""
	def __init__(self, x=0, y=0):
		super(Point, self).__init__()
		self.x = float(x)
		self.y = float(y)


def getIntersection(x1, x2, x3, x4):
	# 두 점을 지나는 직선 끼리의 교점을 찾는 함수.
	# 평행 여부 확인
	parallel1 = (x1.x == x2.x)
	parallel2 = (x3.x == x4.x)
	# result init
	result = Point()
	
	# 직선 1이 y축에 평행한 경우
	if(parallel1):
		sameValue1 = x1.x
	else:
		increase1 = (x2.y - x1.y)/(x2.x - x1.x) # 직선 1의 기울기
		constant1 = x1.y - increase1 * x1.x # 직선 1의 y절편
	
	# 직선 2가 y축에 평행한 경우
	if(parallel2):
		sameValue2 = x3.x
	else:
		increase2 = (x4.y - x3.y)/(x4.x - x3.x) # 직선 2의 기울기
		constant2 = x3.y - increase2 * x3.x # 직선 2의 y절편

	# 두 직선이 평행한 경우 교점 없음. return None
	if(parallel1 and parallel2):
		return None
	
	# 직선 1이 y축에 평행한 경우 직선 1의 직선 위에 교점의 x값이 존재.
	# 직선 2의 y = ax + b 함수에 x값을 넣어 y값을 구함.
	if(parallel1):
		result = Point(sameValue1, increase2 * sameValue1 + constant2)
	# 직선 2가 y축에 평행한 경우 직선 2의 직선 위에 교점의 x값이 존재.
	# 직선 1의 y = ax + b 함수에 x값을 넣어 y값을 구함.
	elif(parallel2):
		result = Point(sameValue2, increase1 * sameValue2 + constant1)
	# y축에 평행한 직선이 없는 경우
	# x = -(b1 - b2)/(a1 - a2) 를 이용하여 x를 구하고 직선 1에 x값을 대입하여 y를 구함.
	else:
		result.x = -(constant1 - constant2)/(increase1- increase2)
		result.y = increase1 * result.x + constant1
	return result
  
print("[*] Input Point(x, y) : ")
a = input()
a = Point(a[0], a[-1])

b = input()
b = Point(b[0], b[-1])

c = input()
c = Point(c[0], c[-1])

d = input()
d = Point(d[0], d[-1])

print(" a : ", a.x, a.y)
print(" b : ", b.x, b.y)
print(" c : ", c.x, c.y)
print(" d : ", d.x, d.y)
print(" Calculate--------")
e = getIntersection(a, b, c, d)
print("-> e : ", e.x, e.y)
