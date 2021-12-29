
LED_COLUMN = 3
LED_ROW = 3      # Number of LED pixels.


# def map_matrix(x, y):
#   if x + 1 <= 1:
#         return y
#  elif x + 1 % 2 == 0:
#         return (x +1)* LED_COLUMN
#  else:
#         return x * y - x


def map_matrix(x, y):
    if x < 1:
        indexValue = y
    elif (x + 1) % 2 == 0:
        indexValue = (x+1)*LED_ROW - y - 1
    else:
        indexValue = x*LED_ROW + y
    # print(str(x) + ";" + str(y) + ";" + str(indexValue))
    return indexValue


for y in range(LED_COLUMN):
    for x in range(LED_ROW):
        print(str(x) + ";" + str(y) + ";" + str(map_matrix(x, y)))
