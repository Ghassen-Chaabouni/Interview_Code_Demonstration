from profil import launch
from contextlib import suppress


# with suppress(OSError):
#     x = launch('realdonaldtrump' , start_time='7/7/2020')

#     print(' ====== ')
#     print(type(x))
#     print(x)


try :

    x = launch('realdonaldtrump' , start_time='3/8/2020')

    print(' ====== ')
    print(type(x))
    print(x)
# import sys
# sys.exit("Error message")
except:
    pass
