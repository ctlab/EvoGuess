from uuid import uuid4
from collections import namedtuple
from structure.array import Backdoor


class UnsupportedTypeError(Exception):
    """The type is unsupported."""
    pass


class BackdoorCache:
    def __init__(self, output):
        self._cache = {}
        self._output = output

        self.index = output.register('backdoors')

    def __contains__(self, backdoor):
        if not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        return key in self._cache

    def __getitem__(self, backdoor):
        if not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        # todo: cut payload
        return self._cache[key][1]

    def __setitem__(self, backdoor, payload):
        if not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        # todo: check payload
        self._cache[key] = backdoor, payload

    def get(self, backdoor, default=None):
        if self.__contains__(backdoor):
            return self.__getitem__(backdoor)
        return default

    def finalize(self, backdoor: Backdoor):
        if not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        info = {
            'uuid': uuid4().hex,
            'key': str(backdoor),
        }
        _, payload = self._cache[info['key']]
        info['count'] = len(payload[0])
        strings = [
            # 'UUID: %s' % info['uuid'],
            'Backdoor: %s' % backdoor,
            'Cases (%d): ' % len(payload[0]),
            *map(str, payload[0]),
            'Time: %.7g' % payload[1]['time'],
            'Estimation: %.7g' % payload[1]['value']
        ]
        self._output.store(self.index, info['uuid'], *strings)
        self._output.write('backdoors.list', str(info))
