import datetime
import json

class MetaData:
    """
    """
    _timeformat="%Y-%m-%dT%H:%M"


    def __init__(self, name):
        """
        """
        self.name=name
        self._now=datetime.datetime.utcnow()
        self.created_at=self._now.strftime(self._timeformat)


class dataExtractor(MetaData):
    """
    """
    def __init__(self, name, target_keys, data_key, owner_name, owner_type):
        """
        """
        super().__init__(name)
        self.target_keys=[t.strip() for t in target_keys.split(";")]
        self.data_key=data_key
        self.owner_name=owner_name
        self.owner_type=owner_type


class ElementGrabber(MetaData):
    """
    """
    def __init__(self, name, selector, selector_type):
        """
        """
        super().__init__(name)
        self.selector=selector
        self.selector_type=selector_type


class ContainerSelector:
    """
    """
    pass

class Action:
    """
    """
    pass

class PostAction:
    """
    """
    pass

class Sequence:
    """
    """
    pass

class Driver:
    """
    """
    pass
