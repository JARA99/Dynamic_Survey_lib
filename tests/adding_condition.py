class hello:
    def __init__(self):
        self.func = None
        self.message = 'hello'
    def set_func(self,f):
        self.func = f
hola = hello
hola
hola = hello()
hola
hola.message
hola.func
hola.set_func(False)
hola.func
def pair():
    return False
hola.set_func(pair)
hola.func
hola.set_func(pair())
hola.func
def rt():
    return True
hola.set_func(rt)
hola.func
hola.func()
def see_text(text):
    if text == hola.message:
        return True
    else:
        return False
def see_text(self,text):
    if text == self.message:
        return True
    else:
        return False
hola.set_func(see_text)
hola.func
hola.func('adios')
hola.func(self,'adios')
get_ipython().run_line_magic('clear', '')
class hello:
    def __init__(self):
        self.func = f
        self.message = 'hello'
class hello:
    def __init__(self):
        self.func = rt
        self.message = 'hello'
    def condition(self,*args,**kargs):
        return self.func(self,*args,**kargs)
    def set_func(self,f):
        self.func = f
rt
rt()
def FUNC_TRUE(*args,**kargs):
    return True
class hello:
    def __init__(self):
        self.func = FUNC_TRUE
        self.message = 'hello'
    def condition(self,*args,**kargs):
        return self.func(self,*args,**kargs)
    def set_func(self,f):
        self.func = f
a = hello()
a
a.message
a.func
a.func()
class hello:
    def __init__(self):
        self._func = FUNC_TRUE
        self.message = 'hello'
    def condition(self,*args,**kargs):
        return self._func(self,*args,**kargs)
    def set_func(self,f):
        self._func = f
a = hello()
a
a.condition
a.condition()
def FUNC_FALSE(*args,**kargs):
    return False
a.set_func(FUNC_FALSE)
a.condition()
def message_same(self,text):
    if text == self.message:
        return True
    else:
        return False
a.condition()
a.condition('hola')
a.message
a.condition('hello')
a.set_func(message_same)
a.condition('hello')
a.condition()
a.condition('bye')
def message_same(self,text:str = ''):
    if text == self.message:
        return True
    else:
        return False
a.condition()
a.set_func(message_same)
a.condition()
get_ipython().run_line_magic('history', '-f /home/jorgealejandro/Documents/EPS2023/Dynamic_Survey_lib/tests/adding_condition.py')

class bye:
    def __init__(self):
        self.origin = None
    def add_origin(self,origin):
        self.origin = origin
b = bye()
b
a
class hello:
    def __init__(self):
        self._func = FUNC_TRUE
        self.message = 'hello'
    def condition(self,*args,**kargs):
        return self._func(self,*args,**kargs)
    def set_func(self,f):
        self._func = f
    def set_as_origin_of(self,other):
        other.add_origin(self)
a = hello()
b
b = bye()
a.set_as_origin_of(b)
b.origin
b.origin()
a.set_func(FUNC_FALSE)
a.condition()
b.origin.condition()
a.set_func(FUNC_TRUE)
b.origin.condition()
a.condition()
get_ipython().run_line_magic('history', '-f /home/jorgealejandro/Documents/EPS2023/Dynamic_Survey_lib/tests/adding_condition.py')
hello
hello.set_func(FUNC_FALSE)
class hello:
    
    instances = []
    
    def set_all_func(f):
        for instance in hello.instances:
            instance.set_func(f)
    
    def __init__(self):
        self._func = FUNC_TRUE
        self.message = 'hello'
        hello.instances.append(self)
        
    def condition(self,*args,**kargs):
        return self._func(self,*args,**kargs)
    
    def set_func(self,f):
        self._func = f
    
    def set_as_origin_of(self,other):
        other.add_origin(self)
a = hello()
a1 = hello()
a2 = hello()
a3 = hello()
a.set_func(FUNC_FALSE)
for instance in hello.instances:
    print(instance.condition())
hello.set_all_func(FUNC_FALSE)
for instance in hello.instances:
    print(instance.condition())
import random as rnd
hellos = [a,a1,a2,a3]
rnd.choices(hellos)
rnd.choices(hellos,k=2)
qs = rnd.choices(hellos,k=2)
qs
qs[0].message
a1.message='a1'
a2.message='a2'
a3.message = 'a3'
qs[0].message
qs[1].message
rnd.randint()
rnd.randint(0,5)
hello.set_all_func(rnd.rndint)
hello.set_all_func(rnd.randint)
a1.condition()
a1.condition(0,5)
class hello:
    
    instances = []
    
    def set_all_func(f):
        for instance in hello.instances:
            instance.set_func(f)
    
    def __init__(self):
        self._func = FUNC_TRUE
        self.message = 'hello'
        hello.instances.append(self)
        
    def condition(self,*args,**kargs):
        return self._func(*args,**kargs)
    
    def set_func(self,f):
        self._func = f
    
    def set_as_origin_of(self,other):
        other.add_origin(self)
a = hello()
a.set_func(message_same)
a.condition()
l = ['a','b','c']
l.index('a')
l.index('b')
l = ['a','b','c','d','b']
l = ['a','b','c','d','b']
l.index('b')
l
l.remove('c')
l
l.remove('c')
l.remove('b')
l
l
'd' in l
l.append(a)
a
a1
a1 in l
a in l
l.index(a)
l
np.mean([])
import numpy as np
np.mean([])
np.mean([])
l
l + [5]
l += [4]
l
l += []
l
l += 4
class mylist(list):
    def __init__(self,l:list = None):
        super().__init__(list)
    def get_probs(self):
        probs = []
        for i in self:
            probs.append('hola: {}'.format(i))
n = mylist()
n = mylist([])
n = mylist([1])
class mylist(list):
    def __init__(self,l:list = []):
        super().__init__(l)
    def get_probs(self):
        probs = []
        for i in self:
            probs.append('hola: {}'.format(i))
n = mylist()
n
n = mylist(5)
n = mylist([5])
n
n.get_probs()
class mylist(list):
    def __init__(self,l:list = []):
        super().__init__(l)
    def get_probs(self):
        probs = []
        for i in self:
            probs.append('hola: {}'.format(i))
        return probs
n.get_probs()
n = mylist([5])
n.get_probs()
get_ipython().run_line_magic('history', '-f /home/jorgealejandro/Documents/EPS2023/Dynamic_Survey_lib/tests/adding_condition.md -o -p -t')
get_ipython().run_line_magic('history', '-f /home/jorgealejandro/Documents/EPS2023/Dynamic_Survey_lib/tests/adding_condition.py -t')
