import itertools

class Ranges:

	def __init__(self, points=None):
		self.ranges = []
		if not points: # None or []
			pass
		elif isinstance(points[0], range):
			self.ranges = points
		else:
			self._sequence = points
			self.createRanges()

	def createRanges(self):
		start = stop = None
		prev_point = self._sequence[0]
		for point in self._sequence:
			if point != prev_point+1:
				if stop:
					self.ranges.append(range(start, stop))
				start = point
				stop = point + 1
			else:
				stop = point + 1
			prev_point = point
		self.ranges.append(range(start, stop))

	def __repr__(self):
		return 'Ranges({})'.format(self.ranges)

	def __len__(self):
		return sum(len(r) for r in self.ranges)

	def __iter__(self):
		return itertools.chain.from_iterable(self.ranges)

	def getOverlapped(self, range_list):
		overlapped = []
		for r1 in range_list:
			for r0 in self.ranges[0:]:
				o_range = range(max(r0.start, r1.start), min(r0.stop, r1.stop))
				if o_range:
					overlapped.append(o_range)
		return Ranges(overlapped)

	def getOverlappedList(self, range_list_list):
		all_overlapped = []
		range_limit = len(self.ranges)-1
		ix0 = 0
		for range_list in range_list_list:
			overlapped = []
			for r1 in range_list:
				while True:
					r0 = self.ranges[ix0]
					o_range = range(max(r0.start, r1.start), min(r0.stop, r1.stop))
					if o_range:
						overlapped.append(o_range)
					if r0.stop >= r1.stop or ix0 >= range_limit:
						break
					ix0 += 1
			all_overlapped.append(Ranges(overlapped))
		return all_overlapped
