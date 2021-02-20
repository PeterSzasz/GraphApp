# simple stack module

class stack:
  '''simple stack, with push n pop n peek'''

  def __init__(self):
    self.dataplates = []
    self.size = 0

  def pop(self):
    last_element = self.dataplates[self.size-1]
    self.size -= 1
    self.dataplates.remove[self.size-1]
    return last_element

  def push(self, element):
    self.dataplates.append(element)
    self.size += 1

  def peek(self):
    return self.dataplates[self.size]

  def size(self):
    return self.size