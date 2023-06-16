from machine import Pin
import utime
 
# Connect Keypad pins as below
col_list = [0, 1, 2, 3]
row_list = [21, 22, 26, 27]
pin_digits = []
correct_pin = [1, 2, 3, 4]
 
# Set rows pin as output
for x in range(0, 4):
    row_list[x] = Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)
 
# Set columns as input
for x in range(0, 4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)
 
# Create a map between keypad buttons and chars
key_map = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]
 
def Keypad4x4Read(cols, rows):
    for r in rows:
        r.value(1)
        result = [cols[0].value(), cols[1].value(), cols[2].value(), cols[3].value()]
        if max(result) == 1:
            key = key_map[int(rows.index(r))][int(result.index(1))]
            r.value(0)  # manages key kept pressed
            return key
        r.value(0)
 
 
# Start the main loop
print("--- Ready to get user inputs ---")
while True:
    key = Keypad4x4Read(col_list, row_list)
    if key != None:
        print("Pressed button: " + key)
        if key.isdigit():
            pin_digits.append(int(key))
            if len(pin_digits) == 4:
                if pin_digits == correct_pin:
                    print("Correct password")
                else:
                    print("Incorrect password")
                pin_digits = []  # Reset the entered digits
        utime.sleep(0.3)  # Gives the user enough time to release without having double inputs (known as debounce)

