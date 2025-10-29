print(20 * "*")
amountOfBeers = 3
beerName = "Somersby"
beerPrice = 2.99
veryBigAlinea = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer maximus eget quam vitae egestas. In ex ligula, molestie sodales ante eu, laoreet euismod purus. Aenean scelerisque ante vel viverra tincidunt. Suspendisse potenti. Cras quis aliquam lacus, quis lobortis ipsum. Nulla euismod rhoncus orci id consequat. Nullam lectus justo, venenatis ut accumsan id, tincidunt at leo.
"""

# print(len(veryBigAlinea))
print(beerName[0])  # first char
print(beerName[-1])  # last char
print(beerName[0:5])  # 5 first chars

####################################
print()
####################################

if (12 > 6):
    print("boop")

print("this is", 3, "parts of a sentence")

iAmCastToAString = str(3)
print(type(iAmCastToAString))

####################################
print()
####################################

x, y, z = "beep", "boop", "burp"


def oneCoolFunction():
    print("hello", y)


oneCoolFunction()


def aLongerFunction():
    global var1
    var1 = 123
    var2 = 456
    print(var1, "followed by", var2)


aLongerFunction()

####################################
print()
####################################

myList = ["beep", "boop", "burp"]

for x in "python":
    print(x)
