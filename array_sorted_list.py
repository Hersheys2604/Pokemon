"""
    Array-based implementation of SortedList ADT.
    Items to store should be of time ListItem.
"""

from referential_array import ArrayR
from sorted_list import *

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev and Graeme Gange'
__docformat__ = 'reStructuredText'

class ArraySortedList(SortedList[T]):
    """ SortedList ADT implemented with arrays. """
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int) -> None:
        """ ArraySortedList object initialiser. """

        # first, calling the basic initialiser
        SortedList.__init__(self)

        # initialising the internal array
        size = max(self.MIN_CAPACITY, max_capacity)
        self.array = ArrayR(size)

    def reset(self):
        """ Reset the list. """
        SortedList.__init__(self)

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        return self.array[index]

    def __setitem__(self, index: int, item: ListItem) -> None:
        """ Magic method. Insert the item at a given position,
            if possible (!). Shift the following elements to the right.
        """
        # if self.is_empty() or \
        #         (index == 0 and item.key <= self[index].key) or \
        #         (index == len(self) and self[index - 1].key <= item.key) or \
        #         (index > 0 and self[index - 1].key <= item.key <= self[index].key):

        #     if self.is_full():
        #         self._resize()

        #     self._shuffle_right(index)
        #     self.array[index] = item
        # else:
        #     # the list isn't empty and the item's position is wrong wrt. its neighbourghs
        #     raise IndexError('Element should be inserted in sorted order')
        if self.is_empty() or \
                (index == 0 and item <= self[index]) or \
                (index == len(self) and self[index - 1] <= item) or \
                (index > 0 and self[index - 1] <= item <= self[index]):

            if self.is_full():
                self._resize()

            self._shuffle_right(index)
            self.array[index] = item
        else:
            # the list isn't empty and the item's position is wrong wrt. its neighbourghs
            raise IndexError('Element should be inserted in sorted order')

    def __contains__(self, item: ListItem):
        """ Checks if value is in the list. """
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def _shuffle_right(self, index: int) -> None:
        """ Shuffle items to the right up to a given position. """
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def _shuffle_left(self, index: int) -> None:
        """ Shuffle items starting at a given position to the left. """
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def _resize(self) -> None:
        """ Resize the list. """
        # doubling the size of our list
        new_array = ArrayR(2 * len(self.array))

        # copying the contents
        for i in range(self.length):
            new_array[i] = self.array[i]

        # referring to the new array
        self.array = new_array

    def delete_at_index(self, index: int) -> ListItem:
        """ Delete item at a given position. """
        if index >= len(self):
            raise IndexError('No such index in the list')
        item = self.array[index]
        self.length -= 1
        self._shuffle_left(index)
        return item

    def index(self, item: ListItem) -> int:
        """ Find the position of a given item in the list. """
        pos = self._index_to_add(item)
        if pos < len(self) and self[pos] == item:
            return pos
        raise ValueError('item not in list')

    def is_full(self):
        """ Check if the list is full. """
        return len(self) >= len(self.array)

    def add(self, item: ListItem) -> None:
        """ Add new element to the list. """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self._index_to_add(item)

        self[position] = item
        self.length += 1

    def _index_to_add(self, item: ListItem) -> int:
        """ Find the position where the new item should be placed. """
        # low = 0
        # high = len(self) - 1

        # while low <= high:
        #     mid = (low + high) // 2
        #     if self[mid].key < item.key:
        #         low = mid + 1
        #     elif self[mid].key > item.key:
        #         high = mid - 1
        #     else:
        #         return mid

        # return low
        low = 0
        high = len(self)-1

        while low <= high:
            mid  = (low + high)//2
            if self[mid] < item:
                low = mid + 1
            elif self[mid] > item:
                high = mid - 1
            else:
                return mid
        return low


class ArraySortedListBattle2(SortedList[T]):
    """ SortedList ADT implemented with arrays. """
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int, criterion_value, special_numb) -> None:
        """ ArraySortedList object initialiser. """

        # first, calling the basic initialiser
        SortedList.__init__(self)

        # initialising the internal array
        size = max(self.MIN_CAPACITY, max_capacity)
        self.array = ArrayR(max_capacity)

        self.criterion_value = criterion_value

        self.special_mode = special_numb

        self.PokeDex = ['Charmander', 'Charizard', 'Bulbasaur', 'Venusaur', 'Squirtle', 'Blastoise', 'Gastly', 'Haunter', 'Gengar', 'Eevee']
        

    def reset(self):
        """ Reset the list. """
        SortedList.__init__(self)

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        return self.array[index]

    def __setitem__(self, index: int, item: ListItem) -> None:
        """ Magic method. Insert the item at a given position,
            if possible (!). Shift the following elements to the right.
        """
        if self.special_mode % 2 == 0:
            if self.criterion_value == 1: #Speed, HP, Level, defence
                if self.is_empty() or \
                        (index == 0 and item.get_speed() > self[index].get_speed()) or \
                        (index == len(self) and self[index - 1].get_speed() > item.get_speed()) or \
                        (index > 0 and self[index - 1].get_speed() > item.get_speed() > self[index].get_speed()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_speed() == self[index].get_speed()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_speed() == item.get_speed()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 2:
                if self.is_empty() or \
                        (index == 0 and item.get_hp() > self[index].get_hp()) or \
                        (index == len(self) and self[index - 1].get_hp() > item.get_hp()) or \
                        (index > 0 and self[index - 1].get_hp() > item.get_hp() > self[index].get_hp()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_hp() == self[index].get_hp()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_hp() == item.get_hp()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 3:
                if self.is_empty() or \
                        (index == 0 and item.get_level() > self[index].get_level()) or \
                        (index == len(self) and self[index - 1].get_level() > item.get_level()) or \
                        (index > 0 and self[index - 1].get_level() > item.get_level() > self[index].get_level()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_level() == self[index].get_level()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_level() == item.get_level()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 4:
                if self.is_empty() or \
                        (index == 0 and item.get_defence() > self[index].get_defence()) or \
                        (index == len(self) and self[index - 1].get_defence() > item.get_defence()) or \
                        (index > 0 and self[index - 1].get_defence() > item.get_defence() > self[index].get_defence()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_defence() == self[index].get_defence()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_defence() == item.get_defence()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
        else:
            if self.criterion_value == 1: #Speed, HP, Level, defence
                if self.is_empty() or \
                        (index == 0 and item.get_speed() < self[index].get_speed()) or \
                        (index == len(self) and self[index - 1].get_speed() < item.get_speed()) or \
                        (index > 0 and self[index - 1].get_speed() < item.get_speed() < self[index].get_speed()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_speed() == self[index].get_speed()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_speed() == item.get_speed()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 2: #Speed, HP, Level, defence
                if self.is_empty() or \
                        (index == 0 and item.get_hp() < self[index].get_hp()) or \
                        (index == len(self) and self[index - 1].get_hp() < item.get_hp()) or \
                        (index > 0 and self[index - 1].get_hp() < item.get_hp() < self[index].get_hp()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_hp() == self[index].get_hp()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_hp() == item.get_hp()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 3: #Speed, HP, Level, defence
                if self.is_empty() or \
                        (index == 0 and item.get_level() < self[index].get_level()) or \
                        (index == len(self) and self[index - 1].get_level() < item.get_level()) or \
                        (index > 0 and self[index - 1].get_level() < item.get_level() < self[index].get_level()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_level() == self[index].get_level()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_level() == item.get_level()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            elif self.criterion_value == 4: #Speed, HP, Level, defence
                if self.is_empty() or \
                        (index == 0 and item.get_defence() < self[index].get_defence()) or \
                        (index == len(self) and self[index - 1].get_defence() < item.get_defence()) or \
                        (index > 0 and self[index - 1].get_defence() < item.get_defence() < self[index].get_defence()):

                    if self.is_full():
                        self._resize()

                    self._shuffle_right(index)
                    self.array[index] = item
                elif (item.get_defence() == self[index].get_defence()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(item.get_poke_name()) <= self.PokeDex.index(self[index].get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index+1)
                        self.array[index+1] = item
                elif (self[index - 1].get_defence() == item.get_defence()):
                    if self.is_full():
                        self._resize()
                    if self.PokeDex.index(self[index-1].get_poke_name()) <= self.PokeDex.index(item.get_poke_name()):
                        self._shuffle_right(index)
                        self.array[index] = item
                    else:
                        self._shuffle_right(index-1)
                        self.array[index-1] = item
                else:
                    # the list isn't empty and the item's position is wrong wrt. its neighbourghs
                    raise IndexError('Element should be inserted in sorted order')
            
    def __contains__(self, item: ListItem):
        """ Checks if value is in the list. """
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def _shuffle_right(self, index: int) -> None:
        """ Shuffle items to the right up to a given position. """
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def _shuffle_left(self, index: int) -> None:
        """ Shuffle items starting at a given position to the left. """
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def _resize(self) -> None:
        """ Resize the list. """
        # doubling the size of our list
        new_array = ArrayR(2 * len(self.array))

        # copying the contents
        for i in range(self.length):
            new_array[i] = self.array[i]

        # referring to the new array
        self.array = new_array

    def delete_at_index(self, index: int) -> ListItem:
        """ Delete item at a given position. """
        if index >= len(self):
            raise IndexError('No such index in the list')
        item = self.array[index]
        self.length -= 1
        self._shuffle_left(index)
        return item

    def index(self, item: ListItem) -> int:
        """ Find the position of a given item in the list. """
        pos = self._index_to_add(item)
        if pos < len(self) and self[pos] == item:
            return pos
        raise ValueError('item not in list')

    def is_full(self):
        """ Check if the list is full. """
        return len(self) >= len(self.array)

    def add(self, item: ListItem) -> None:
        """ Add new element to the list. """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self._index_to_add(item)

        self[position] = item
        self.length += 1

    def _index_to_add(self, item: ListItem) -> int:
        """ Find the position where the new item should be placed. """
        # low = 0
        # high = len(self) - 1

        # while low <= high:
        #     mid = (low + high) // 2
        #     if self[mid].key < item.key:
        #         low = mid + 1
        #     elif self[mid].key > item.key:
        #         high = mid - 1
        #     else:
        #         return mid

        # return low
        if self.special_mode % 2 == 0:
            if not self.is_empty():
                if self.criterion_value == 1:
                    low = 0
                    high = len(self)-1

                    while low <= high:
                        mid  = (low + high)//2
                        if self[mid].get_speed() > item.get_speed():
                            low = mid + 1
                        elif self[mid].get_speed() < item.get_speed():
                            high = mid - 1
                        else:
                            return mid
                    return low
                elif self.criterion_value == 2:
                    low = 0
                    high = len(self)-1

                    while low <= high:
                        mid  = (low + high)//2
                        if self[mid].get_hp() > item.get_hp():
                            low = mid + 1
                        elif self[mid].get_hp() < item.get_hp():
                            high = mid - 1
                        else:
                            return mid
                    return low
                elif self.criterion_value == 3:
                    low = 0
                    high = len(self)-1

                    while low <= high:
                        mid  = (low + high)//2
                        if self[mid].get_level() > item.get_level():
                            low = mid + 1
                        elif self[mid].get_level() < item.get_level():
                            high = mid - 1
                        else:
                            return mid
                    return low
                elif self.criterion_value == 4:
                    low = 0
                    high = len(self)-1

                    while low <= high:
                        mid  = (low + high)//2
                        if self[mid].get_defence() > item.get_defence():
                            low = mid + 1
                        elif self[mid].get_defence() < item.get_defence():
                            high = mid - 1
                        else:
                            return mid
                    return low
            else:
                return 0
        else:
            if self.criterion_value == 1:
                low = 0
                high = len(self)-1

                while low <= high:
                    mid  = (low + high)//2
                    if self[mid].get_speed() < item.get_speed():
                        low = mid + 1
                    elif self[mid].get_speed() > item.get_speed():
                        high = mid - 1
                    else:
                        return mid
                return low
            elif self.criterion_value == 2:
                low = 0
                high = len(self)-1

                while low <= high:
                    mid  = (low + high)//2
                    if self[mid].get_hp() < item.get_hp():
                        low = mid + 1
                    elif self[mid].get_hp() > item.get_hp():
                        high = mid - 1
                    else:
                        return mid
                return low
            elif self.criterion_value == 3:
                low = 0
                high = len(self)-1

                while low <= high:
                    mid  = (low + high)//2
                    if self[mid].get_level() < item.get_level():
                        low = mid + 1
                    elif self[mid].get_level() > item.get_level():
                        high = mid - 1
                    else:
                        return mid
                return low
            elif self.criterion_value == 4:
                low = 0
                high = len(self)-1

                while low <= high:
                    mid  = (low + high)//2
                    if self[mid].get_defence() < item.get_defence():
                        low = mid + 1
                    elif self[mid].get_defence() > item.get_defence():
                        high = mid - 1
                    else:
                        return mid
                return low

    def special_mode_increment(self):
        self.special_mode += 1
