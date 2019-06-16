from copy import deepcopy
from time import time, strftime, sleep
from threading import Thread
from math import floor

class Node(object):

    def __init__(self, data, next=None, previous=None):
        self.data = data
        self.next = next
        self.previous = previous

    def set_next(self, next):
        self.next = next

    def set_data(self, data):
        self.data = data


class LinkedList(object):

    def __init__(self, root=None):
        self.root = root
        self.current_node = self.root
        self.size = 0

    def __repr__(self):
        return str(self.current_node.data)

    def add(self, data):
        node = Node(data)
        node.next = self.root

        if self.root is not None:
            self.root.previous = node

        self.root = node
        self.current_node = node
        self.size += 1

    def remove(self, data):
        node = self.root
        prev = None

        while node is not None:
            if node.data == data:
                if prev:
                    prev.set_next(node.next)
                else:
                    self.root = node
                self.size -= 1
                return True
            else:
                prev = node
                node = node.next
        return False

    def find(self, data):
        node = self.root
        while node is not None:
            if node.data == data:
                return node
            else:
                node = node.next
        return None

    def print(self):
        node = self.root
        while node is not None:
            print("%d" % node.data, end=" ")
            node = node.next
        print()
        del node

    def next(self):
        if self.current_node.next is not None:
            self.current_node = self.current_node.next
            return True
        else:
            return False

    def hasNext(self, node):
        if node.next is None:
            return False
        else:
            return True


class Array:

    def __init__(self, slots, initialize=None):
        self.length = slots
        self.data = [initialize] * slots

    def set(self, pos, val=None, function=None):
        if pos < self.length - 1 and pos >= 0:
            if function is not None and val is None:
                self.data[pos] = function(self.data[pos])
            elif function is None and val is not None:
                self.data[pos] = val

    def get(self):
        return self.data

    def getValue(self, index):
        return self.data[index]

    def search(self, value):
        indexes = []
        for index, data in enumerate(self.data):
            if data == value:
                indexes.append(index)
        if len(indexes) == 1:
            return indexes[0]
        elif len(indexes) == 0:
            return None
        else:
            return indexes

    def remove(self, index, value=None):
        if index < self.length and index >= 0 and type(index) == int and value is None:
            self.data.pop(index)
        elif value is not None:
            newArr = self.copy()
            for _ in newArr.search(value):
                newArr.data.remove(value)
            return newArr
        else:
            raise IndexError

    def copy(self):
        return deepcopy(self)

    @staticmethod
    def listToArray(a):
        if type(a) is list:
            newArray = Array(len(a), 0)
            newArray.data = deepcopy(a)
            newArray.length = len(a)
            return newArray

    def swap(self, i, j):
        value = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = value
        del value

    def reverse(self):
        test = reversed(deepcopy(self.data))
        self.data = test
        del test

    def concat(self, data):
        test = deepcopy(self.data) + data
        self.data = test
        del test

    def splice(self, index):
        value = self.getValue(index)
        self.remove(index)
        newList = []
        newList.append(value)
        del value
        return newList

    def print(self):
        for d in self.data:
            print(d, end=" ")
        print()


class Sorting:

    def __init__(self, arr):
        self.array = arr
        self.original = arr
        self.history = []
        self.length = len(self.array)

    def __repr__(self):
        return str(self.array)

    def get(self):
        return self.array

    def BubbleSort(self, reverse=False):
        a = deepcopy(self)
        start = time()
        for i in range(a.length):
            for j in range(a.length):
                if not reverse:
                    if a.array[i] < a.array[j]:
                        aux = a.array[i]
                        a.array[i] = a.array[j]
                        a.array[j] = aux
                        a.history.append(deepcopy(a.array))
                else:
                    if a.array[i] > a.array[j]:
                        aux = a.array[i]
                        a.array[i] = a.array[j]
                        a.array[j] = aux
                        a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("BubbleSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def InsertionSort(self, save=False):
        a = deepcopy(self)
        start = time()
        for i in range(1, a.length):
            key = a.array[i]
            j = i-1
            while j >= 0 and key < a.array[j]:
                a.array[j + 1] = a.array[j]
                j -= 1
                if save:
                    a.history.append(deepcopy(a.array))
            a.array[j + 1] = key
            if save:
                a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("InsertionSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def QuickSort(self):
        a = deepcopy(self)
        start = time()
        self.__quicks(a.array, 0, a.length-1)
        end = time()
        print("Algorithm: {}".format("QuickSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def __countingSort(self, arr, exp1):
        n = len(arr)
        output = [0] * (n)
        count = [0] * (10)

        for i in range(0, n):
            index = (arr[i]/exp1)
            count[(index) % 10] += 1

        for i in range(1, 10):
            count[i] += count[i-1]

        i = n-1
        while i >= 0:
            index = int(arr[i]/exp1)
            output[count[(index) % 10] - 1] = arr[i]
            count[(index) % 10] -= 1
            i -= 1
        i = 0
        for i in range(0, len(arr)):
            arr[i] = output[i]

    def RadixSort(self):
        a = deepcopy(self)
        start = time()
        max1 = max(a.array)
        exp = 1
        while max1 / exp > 0:
            self.__countingSort(a.array, exp)
            exp *= 10
        end = time()
        print("Algorithm: {}".format("RadixSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def __quicks(self, arr, low, high):
        if low < high:
            pi = self.__partition(arr, low, high)
            self.__quicks(arr, low, pi-1)
            self.__quicks(arr, pi+1, high)

    def __partition(self, arr, low, high):
        i = low - 1
        pivot = arr[high]

        for j in range(low, high):
            if arr[j] <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i + 1)

    def ShellSort(self):
        a = deepcopy(self)
        gap = a.length//2
        start = time()
        while gap > 0:
            for i in range(gap, a.length):
                temp = a.array[i]
                j = i
                while j >= gap and a.array[j-gap] > temp:
                    a.array[j] = a.array[j-gap]
                    j -= gap
                    a.history.append(deepcopy(a.array))
                a.array[j] = temp
                a.history.append(deepcopy(a.array))
            gap //= 2
        end = time()
        print("Algorithm: {}".format("ShellSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def __insertionSort(self, b):
        for i in range(1, len(b)):
            up = b[i]
            j = i - 1
            while j >= 0 and b[j] > up:
                b[j + 1] = b[j]
                j -= 1
            b[j + 1] = up
        return b

    def BucketSort(self):
        a = deepcopy(self)
        start = time()
        arr = []
        slot_num = 10
        for i in range(slot_num):
            arr.append([])
        for j in a.array:
            index_b = int(slot_num * j)
            arr[index_b].append(j)

        for i in range(slot_num):
            arr[i] = self.__insertionSort(arr[i])

        k = 0
        for i in range(slot_num):
            for j in range(len(arr[i])):
                a.array[k] = arr[i][j]
                k += 1
                a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("BucketSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def SelectionSort(self):
        a = deepcopy(self)
        start = time()
        for i in range(a.length):
            min_idx = i
            for j in range(i+1, a.length):
                if a.array[min_idx] > a.array[j]:
                    min_idx = j
            a.array[i], a.array[min_idx] = a.array[min_idx], a.array[i]
            a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("SelectionSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def StoogeSort(self):
        a = deepcopy(self)
        start = time()
        self.__stooge(a.array, 0, a.length-1)
        end = time()
        print("Algorithm: {}".format("StoogeSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def __stooge(self, arr, l, h):
        if l >= h:
            return

        if arr[l] > arr[h]:
            t = arr[l]
            arr[l] = arr[h]
            arr[h] = t

        if h-l + 1 > 2:
            t = (int)((h-l + 1)/3)
            self.__stooge(arr, l, (h-t))
            self.__stooge(arr, l + t, (h))
            self.__stooge(arr, l, (h-t))

    def __getNextGap(self, gap):
        gap = (gap * 10)/13
        if gap < 1:
            return 1
        return int(gap)

    def CombSort(self, save=False):
        a = deepcopy(self)
        start = time()
        n = a.length

        gap = n
        swapped = True

        while gap != 1 or swapped == 1:
            gap = self.__getNextGap(gap)

            swapped = False

            for i in range(0, n-gap):
                if a.array[i] > a.array[i + gap]:
                    a.array[i], a.array[i + gap] = a.array[i + gap], a.array[i]
                    swapped = True
                    if save:
                        a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("CombSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def PigeonholeSort(self, save=False):
        a = deepcopy(self)
        start = time()
        my_min = min(a.array)
        my_max = max(a.array)
        size = my_max - my_min + 1

        holes = [0] * size

        for x in a.array:
            assert type(x) is int, "integers only please"
            holes[x - my_min] += 1
        i = 0
        for count in range(size):
            while holes[count] > 0:
                holes[count] -= 1
                a.array[i] = count + my_min
                i += 1
                if save:
                    a.history.append(deepcopy(a.array))
        end = time()
        print("Algorithm: {}".format("PigeonholeSort"), "|", "Time ellapsed: {}{}".format(
            end-start, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a

    def CocktailSort(self):
        a = deepcopy(self)
        starting = time()
        swapped = True
        start = 0
        end = a.length-1
        while (swapped == True):

            swapped = False

            for i in range(start, end):
                if (a.array[i] > a.array[i + 1]):
                    a.array[i], a.array[i + 1] = a.array[i + 1], a.array[i]
                    swapped = True
                    a.history.append(deepcopy(a.array))

            if (swapped == False):
                break

            swapped = False

            end = end-1

            for i in range(end-1, start-1, -1):
                if (a.array[i] > a.array[i + 1]):
                    a.array[i], a.array[i + 1] = a.array[i + 1], a.array[i]
                    a.history.append(deepcopy(a.array))
                    swapped = True

            start = start + 1

        end = time()
        print("Algorithm: {}".format("CocktailSort "), "|", "Time ellapsed: {}{}".format(
            end-starting, "s"), "|", "Moves: {}".format(len(a.history)), flush=True)
        return a


class TimedList(Thread):

    exec = True

    def __init__(self, timeout=60):
        self.start = time()
        self.timeout = timeout
        self.original = []
        self.list = []
        self.due_items = []
        self.size = 0
        Thread.__init__(self)
        Thread.setName(self, 'TimedList')
        Thread.start(self)

    def add(self, data, timeout=None):
        temp = {
            'data': data,
            'date': {
                'date': strftime('%d/%m/%Y'),
                'time': strftime('%H:%M:%S')
            },
            'time': time(),
            'timeout': timeout if timeout is not None else self.timeout
        }
        self.original.append(temp)
        temp['due'] = False
        self.list.append(temp)
        self.size += 1
        del temp

    def run(self):
        while self.exec:
            self.update()
            self.size = len(self.list)
            sleep(1)

    def update(self):
        to_remove = []
        for index, item in enumerate(self.list):
            if floor(time() - item['time']) >= item['timeout']:
                item['due'] = True
                to_remove.append(index)
        # for item in self.list:
        #  if item['due']:
        #    self.due_items.append(item)
        #self.list = [item for item in self.list if item['due'] is False]
        if len(to_remove) > 0:
            to_remove.sort()
            to_remove.reverse()
            for i in to_remove:
                self.due_items.append(self.list[i])
                print(self.list[i]['date'], strftime('%H:%M:%S'), flush=True)
                self.list.pop(i)
