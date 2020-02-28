# ---Ожидаемый результат---
# <html>
# <head>
#   <title>hello</title>
# </head>
# <body>
#     <h1 class="main-text">Test</h1>
#     <div class="container container-fluid" id="lead">
#         <p>another test</p>
#         <img src="/icon.png" data-image="responsive"/>
#     </div>
# </body>
# </html>

# Таким образом:

# В коде должно быть минимум три основных класса HTML, TopLevelTag и Tag.
# Класс HTML определяет, куда сохранять вывод: на экран через print или в файл.
# Объекты класса TopLevelTag скорее всего не содержат внутреннего текста и всегда парные.
# Объекта класса Tag могут быть непарные или быть парные и содержать текст внутри себя.
# Должна быть возможность задать атрибуты в Tag, но в данном задании для TopLevelTag это необязательное условие.
# Это задание имеет очень гибкие варианты решения, и в первую очередь в решении оценивается результат (получился или не получился HTML как на фрагменте выше). Код, приведенный выше, — просто вариант решения. Возможно, вам проще будет решить задание с другим форматом ввода или создания документа.

# То есть:

# Для решения задания не обязательно использовать контекстный менеджер
# Можно использовать или не использовать наследование
# Можно использовать или не использовать специальные методы
# Можно использовать или не использовать *args/**kwargs для указания решения
# В этом задании обязательно использовать классы. Хотя решение можно получить и просто на функциях, в данном задании использование классов предпочтительней.

class Tag:
    def __init__(self, tag, is_single=False, class_=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        
        self.is_single = is_single
        self.children = []

        if class_ is not None:
            self.attributes["class"] = " ".join(class_)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value        

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback): pass

    def __iadd__(self, child):
        self.children.append(child)
        return self
    
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            if len(attrs) == 0: 
                opening = "<{t}>".format(t=self.tag)
            else: 
                opening = "<{t} {a}>".format(t=self.tag, a=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += "\n" + str(child)
            internal += "\n"
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            else:
                if len(attrs) == 0: 
                    opening = "<{t}>".format(t=self.tag)
                    return "<{t}>{txt}</{t}>".format(
                        t=self.tag, txt=self.text)
                else: 
                    return "<{t} {a}>{txt}</{t}>".format(
                        t=self.tag, a=attrs, txt=self.text)

class TopLevelTag(Tag): 
    def __init__(self, tag):
        self.tag = tag

        self.text = ""
        self.attributes = {}
        
        self.is_single = False
        self.children = []

        self.fp = None

    def __exit__(self, type, value, traceback): 
        pass

class HTML(Tag): 
    def __init__(self, tag, output=None):
        self.tag = tag

        self.text = ""
        self.attributes = {}
        
        self.is_single = False
        self.children = []

        self.fp = None
        if output is not None:
            self.fp = open(output, "w")

    def __exit__(self, type, value, traceback): 
        if self.fp is not None:
            self.fp.write(str(self))
            self.fp.close()
        else:
            print(str(self))

import sys

if __name__ == "__main__":
    if len (sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "B3-13-with.html"

    with HTML("html", output=fn) as html:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello!"
                head += title
            html += head
            
        with TopLevelTag("body") as body:
            with Tag("h1", class_=("main-text",)) as h1:
                h1.text = "Test"
            body += h1
            with Tag("div", class_=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img
            body += div
        html += body

with open(fn) as fp:
    print("Из файла:", fn)
    print(fp.read())