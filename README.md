# pyuoa
Really basic Python "binding" for talking to Razor while playing UO.  Not complete, probably not gonna be complete.  With this, you can get stats and skills and get player coordinates using pywin32.

## Examples
```
>>> from uoa import UOA
>>> uoa = UOA()
>>> print(uoa.get_coords())
{'ns': 2517, 'ew' 3696}
>>> print(uoa.get_stat("str"))
100
>>> print(uoa.get_skill("lumberjacking"))
{'display': 53.6, 'base': 42.1, 'lock': 'U', 'name': 'Lumberjacking'}
>>> print(uoa.is_poisoned())
False
```
