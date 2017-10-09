import time
import hashlib

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
        if "screenshot" in action:
            if not self._raw.get("data"):
                raise AttributeError("[-] Output path is "\
                                     "required for screenshot")
            shot_type=action.split("_")[-1].strip()
            if shot_type == "db": #only works as base64
                self.response.append({"screenshot":self._wd.get_screenshot()})
            self._wd.save_screenshot(self._raw["data"], imgType=shot_type)
            return
        if action == "save_page_source":
            if not self._raw.get("data"):
                url=self._wd.current_url()
                md5=hashlib.md5()
                md5.update(url.encode)
                fileName=md5.hexdump()
            else:
                fileName=self._raw["data"]



    def do(self):
        """
        """
        typis=self._raw["type"]
        if self._raw["scope"] == "element" and not self._wel:
            raise AttributeError("[-] Missing element")
        self._dos[typis]()


class Sequence:
    """
    """

    def __init__(self, movementsList, webdriver, selector=None):
        """

        movementsList
        ----------
        [{
            "index":execution position,
            "selector":"",
            "extractor":"",
            "action":"", #click, page_source, back
            "script":"",
            "data":"" #send keys for example,
            "type":"" #movement type -> grabber, #grab value
                                        script,  #run script
                                        interaction #click, send keys..
            "scope":"" #page or element
          }...]


         selector
         --------
         if selector is set :: the sequence will happen against a
         element[list]
         sequence creator has the responsability to came back to
         the same page state


        """
        self._seq=sorted(movementsList, key=lambda e:e["index"])
        if selector:
            elements=webdriver.xpath(selector)
            if  elements is None: raise Exception("[-] No elements found"\
                                                  " to run sequence")
            for element in elements:
                for seq in self._seq:
                    mv=Movement(webdriver, seq, element)
                    mv.run()
