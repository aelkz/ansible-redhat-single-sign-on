#!/usr/bin/python
from collections import OrderedDict

class FilterModule(object):
    def filters(self):
        return {
            'subkeySort': self.subkeySort,
            'subkeySort2': self.subkeySort2,
            'subkeySort3': self.subkeySort3,
        }

    def subkeySort(self, dict_to_sort, sorting_key):
        return OrderedDict(sorted(dict_to_sort.items(), key=lambda(k,v):(v,k) ))

    def subkeySort2(self, dict_to_sort, sorting_key):
        return OrderedDict(sorted(dict_to_sort.items(), key=lambda x: x[1][sorting_key]))

    def subkeySort3(self, dict_to_sort, sorting_key):
        return sorted(dict_to_sort.items(), key=lambda x: x[1][sorting_key])