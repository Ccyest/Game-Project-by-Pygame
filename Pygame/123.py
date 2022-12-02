# Yichi Zhang
# pcv9ha





def convert(n):
    return int(n)

def divide(a,b):
    try:
        return a/b
    except:
        print('yikes')
        return -1

def convert_divide(q,r):
    thing1 = convert(q)
    thing2 = convert(r)
    print(divide(thing1,thing2))


convert_divide(-5.0,10)


