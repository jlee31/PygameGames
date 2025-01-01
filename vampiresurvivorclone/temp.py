from collections import Counter
def fcn(text):
    counter = Counter(text)
    count = 0
    balloon = "balloon"
    while True:
        for letter in balloon:
            if counter[letter] == 0:
                return count
            counter[letter] -= 1
        count += 1
print(fcn("nlaebolko"))
print(fcn("loonbalxballpoon"))
print(fcn("leetcode"))
    
