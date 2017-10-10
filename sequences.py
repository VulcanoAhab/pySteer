from .movements import Movement

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
                    mv.move()
        else:
            for seq in self._seq:
                mv=Movement(webdriver, seq)
                mv.move()
