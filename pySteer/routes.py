import time
import json

class Augur:
    """
    The seer
    --------
    translator engine
    from config to browser
    interaction
    """
    _elements={}

    _browser=None

    _main_sequence=iter([])

    @classmethod
    def setBrowser(cls, browserObj):
        """
        """
        cls._browser=browserObj


    @classmethod
    def process(cls, configObj):
        """
        """
        main_sequence=configObj.main_sequence
        main_scope=main_sequence["scope"] #will be used soon
        main_pipe=main_sequence["pipe"]
        cls._main_sequence=iter(main_pipe)

        while True:
            try:
                obj=next(cls._main_sequence)
                command=list(obj.keys())[0]
                class_method=getattr(cls, command)
                class_method(**obj[command])
            except StopIteration:
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print("[-] Fail to process: [{}]\n {}".format(e,
                                json.dumps(obj, indent=3)))
                continue

    @classmethod
    def targetedSequence(cls, sequenceObj):
        """
        """
        pass

    @classmethod
    def locate(cls, name, pattern, type):
        """
        """
        print("[+] LOCATE {} WITH {}:{}".format(name, pattern, type))
        try:
            els=getattr(cls._browser,type)(pattern)
        except Exception as e:
            els=[]
            print("[-] Fail to process locate::elements:{}".format(e))
        if not len(els):
            msg="[*] Warning: No elements found for {}".format(pattern)
            print(msg)
        cls._elements[name]={"els":els, "size":len(els)}

    @classmethod
    def extract(cls, target, attribute, field):
        """
        """
        print("[+] EXTRACT {} FROM {}".format(attribute, target))
        _links=["href","src","data-src"]
        els=cls._elements[target]["els"]
        attrs=cls._elements[target]["attrs"]=[]
        if attribute == "text":
            attrs.extend([{field:el.text} for el in els])
        elif attribute == "link":
            for el in els:
                for _l in _links:
                    attr=el.get(_l)
                    if not attr:continue
                    attrs.append({field:attr})
        else:
            attrs.extend([{field:el.get(attribute)} for el in els])

    @classmethod
    def write(cls, into, content):
        """
        """
        print("[+] WRITE {} INTO {}".format(content, into))
        if cls._elements[into]["size"] < 1:
            raise Exception("[-] No objects to write")
        if cls._elements[into]["size"] > 1:
            raise Exception("[-] Can't write on multiple objects")
        el=cls._elements[into]["els"][0]
        el.send_keys(content)

    @classmethod
    def action(cls, name, target=None, value=None):
        """
        """
        print("[+] ACTION {}.".format(name))
        if not target:
            if name == "wait":
                if not value:
                    value=3
                time.sleep(value)
                return
            return getattr(cls._browser, name)()
        if cls._elements[target]["size"] < 1:
            raise Exception("[-] No objects to run action")
        els=cls._elements[target]["els"]
        for el in els:getattr(el, name)()
