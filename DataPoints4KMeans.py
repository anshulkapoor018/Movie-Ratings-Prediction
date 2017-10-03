
file = open("rate.csv", "r")
for line in file:
	data = line.split(' ')
	# print data
	N = []
	for numbers in data:
		try:
			n = float(numbers)
			N.append(n)
		except ValueError:
			pass
	N.pop(0)
        print N
