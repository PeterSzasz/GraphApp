# simple double-ended queue

class queue:
  '''simple queue with enqueue(enq), dequeue(deq), peek'''

  def __init__(self) -> None:
    self.dataplates = []
    self.first = 0  # at the front, deq side
    self.last = 0   # at the back, enq side

  def enqueue(self, element) -> None:
    self.dataplates.append(element)
    self.last += 1

  def dequeue(self):
    front_element = self.dataplates[self.first]
    self.dataplates.remove(self.first)
    self.first += 1
    return front_element

  def peek(self):
    return self.dataplates[self.first]