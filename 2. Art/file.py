from functools import wraps

#Ex1
def greetings(callable):
  @wraps(callable)
  def inner(*args):
    result = callable(*args)
    return "Hello " + result.title()
  return inner
  
#Ex2
from functools import wraps
def is_palindrome(callable):
  @wraps(callable)
  def inner(*args):
    result = callable(*args)
    result2 = ''.join(i for i in result if i.isalnum())
    if result2.lower() == result2[::-1].lower():
      return result + " - is palindrome"
    else:
      return result + " - is not palindrome"
  return inner

#Ex3
def format_output(*args, **kwargs):
  def wrapper(func):
      def wrapper2(*args2, **kwargs2):
          x = func(*args2, **kwargs2)
          result={}
          for i in args:
              if i in x.keys():
                  result[i]=x[i]
              else:
                  y=''
                  s=i.split(sep='__')
                  for sp_arg in s:
                      if sp_arg in x.keys():
                          y=y+x[sp_arg]+" "
                      else:
                          raise ValueError
                  result[i]=y.strip()
          return result
      return wrapper2
  return wrapper
  
#Ex4
def add_class_method(cls):
    def decorator(func):
        @classmethod
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator

def add_instance_method(cls):
    def decorator(func): 
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator
