from machine import Pin
import utime
 
# Connect Keypad pins as below
col_list = [0, 1, 2, 3]
row_list = [21, 22, 26, 27]
states = [False, False, False, False]

# Set rows pin as output
for x in range(0, 4):
    row_list[x] = Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)
 
# Set columns as input
for x in range(0, 4):
    col_list[x] = Pin(col_list[x], Pin.IN)
 
# Create a map between keypad buttons and chars
key_map = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

previousKey = None 
def Keypad4x4Read(cols, rows):
    global states
    i = 0
    for r in rows:
        r.value(1)
        result = [cols[0].value(), cols[1].value(), cols[2].value(), cols[3].value()]
        if max(result) == 1 and states[i] == False:
            key = key_map[int(rows.index(r))][int(result.index(1))]
            r.value(0)  
            states[i] = True
            return key
        states[i] = max(result)
        i = (i + 1) % 4
        r.value(0)
 
