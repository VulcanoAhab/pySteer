class Movement:
    """
    """
    @classmethod
    def _testDict(cls, _raw):
        """
        """
        if not _raw.get("type"):
            raise AttributeError("[-] Type is required")
        typis=self._raw["type"]
        if typis == "grabber":
            if not(self._raw.get("selector")
                   and self._raw.get("extractor")):
                   raise AttributeError("[-] Grabber must have"\
                                    "selector and extractor")
        elif typis == "script":
            if not self._raw.get("script"):
                raise AttributeError("[-] Must set a script to run")
        elif typis == "interaction":
            if not self._raw.get("action"):
                raise AttributeError("[-] Must set action")
        return _raw

    def __init__(self, webdriver, movementDict, webElement=None):
        """
        """
        self._raw=self._testDict(movementDict)
        self._wd=webdriver
        self._wel=webElement
        self._dos={
            "script":self._doScript,
            "interaction":self._doInteraction,
            "grabber":self._doGrabber
        }
        self._response=[]

    def _doScript(self):
        """
        """
        script=self._raw["script"]
        response=self._wd.execute_script(script)
        if isinstance(response, (list, tuple, set)):
            self._response.extend(response)
        else:
            self._response.append(response)

    def _doGrabber(self):
        """
        """
        selector=self._raw["selector"]
        extractor=self._raw["extractor"]
        results=self._wd.xpath(selector, extractor=extractor)
        self._response.extend(results)

    def _doInteraction(self):
        """
        """
        action=self._raw["action"]
        if self._raw["scope"] == "element":
            target=self._wel
        else:
            target=self._wd
        getattr(target, action)(data=self._raw.get("data"))
        

    def do(self):
        """
        """
        typis=self._raw["type"]
        if self._raw["scope"] == "element" and not self._wel:
            raise AttributeError("[-] Missing element")
        self._dos[typis]()
