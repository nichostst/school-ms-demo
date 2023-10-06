from abc import ABC
from typing import List


class Element(ABC):
    __tagname__: str
    __required__: List

    def __init__(self, class_=None, id_=None, **kwargs):
        super().__init__()
        self.class_ = class_
        self.id_ = id_

        self._check_kwargs_validity(kwargs)
        self.kwargs = kwargs

    def _check_kwargs_validity(self, kwargs):
        for req in self.__required__:
            assert req in kwargs


    @property
    def tags(self) -> List[str]:
        tags = []

        if self.class_:
            cstr = f'class="{self.class_}"'
            tags.append(cstr)
        
        if self.id_:
            istr = f'id="{self.id_}"'
            tags.append(istr)

        for kw in self.kwargs:
            kwstr = f'{kw}="{self.kwargs[kw]}"'
            tags.append(kwstr)

        return tags
    
    @property
    def tagstr(self) -> str:
        return ' '.join(self.tags)

    def html(self) -> str:
        pass


class A(Element):
    __tagname__ = 'a'
    __required__ = ['href']

    def __init__(self, text, class_=None, id_=None, **kwargs):
        super().__init__(class_, id_, **kwargs)
        self.text = text

    def html(self):
        return f'<{self.__tagname__} {self.tagstr}>{self.text}</{self.__tagname__}>'


class Button(Element):
    __tagname__ = 'button'
    __required__ = []

    def __init__(self, text: str, class_=None, id_=None, **kwargs):
        super().__init__(class_, id_, **kwargs)
        self.text = text

    def html(self):
        return f'<{self.__tagname__} {self.tagstr}>{self.text}</{self.__tagname__}>'


class Input(Element):
    __tagname__ = 'input'
    __required__ = ['type', 'name']

    def __init__(self, class_=None, id_=None, **kwargs):
        super().__init__(class_, id_, **kwargs)

    def html(self):
        return f'<{self.__tagname__} {self.tagstr}>'
