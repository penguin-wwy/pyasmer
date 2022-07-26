import operator
from typing import Sequence, Tuple, Optional, Callable


class IncDict(dict):

    _inc_count = 0

    def init_by_seq(self, inputs: Sequence) -> 'IncDict':
        for idx, item in enumerate(inputs):
            self[item] = idx
        self._inc_count = 0
        return self

    def to_seq(self) -> Tuple:
        return tuple(kv[0] for kv in sorted(self.items(), key=operator.itemgetter(1)))

    def to_seq_if_inc(self) -> Optional[Tuple]:
        return self.to_seq() if self._inc_count else None

    def __setitem__(self, key, value):
        if key not in self:
            self._inc_count += 1
        super(IncDict, self).__setitem__(key, value)

    @property
    def inc(self):
        return self._inc_count


class DefaultDict(dict):

    _default_func: Callable = lambda: None

    @staticmethod
    def create(f: Callable):
        d = DefaultDict()
        d._default_func = f
        return d

    def __getitem__(self, item):
        if item not in self:
            self.__setitem__(item, self._default_func())
        return super(DefaultDict, self).__getitem__(item)
