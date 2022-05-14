class Stack():
  def _init_(self):
    self._data = []

  def push(self, data):
      self._data.append(data)
  def pop(self):
    return self._data.pop
  def peek(self):
      return self._data[len(self._data)-1]
stack = Stack()
 
