trans = [
    ["apple", "banana", "milk"],
    ["apple", "milk", "banana"],
    ["banana", "milk", "beer"],
    ["apple", "banana", "milk"],
    ["milk", "bread", "rice"],
    ["apple", "bread", "milk"],
    ["milk", "bread", "rice"],
    ["apple", "bread", "milk"],
    ["banana", "bread", "bread"],
    ["chocolate", "milk", "apple"],
    ["banana", "honey", "milk"],
    ["rice", "bread", "milk"],
    ["cheese", "apple", "crackers"],
    ["yogurt", "banana", "granola"],
    ["juice", "bread", "apple"],
    ["beer", "chips", "salsa"],
    ["pasta", "tomato", "basil"],
    ["milk", "cookie", "chocolate"],
    ["fish", "chips", "lemon"],
    ["beef", "carrot", "potato"],
    ["lettuce", "tomato", "cucumber"],
    ["orange", "apple", "banana"],
    ["water", "lime", "mint"],
    ["tea", "honey", "lemon"],
    ["egg", "bacon", "toast"],
    ["rice", "bean", "corn"],
    ["peanut butter", "jelly", "bread"],
    ["chicken", "rice", "broccoli"],
    ["salmon", "asparagus", "lemon"],
    ["milk", "banana", "peanut butter"]
]

transactions = tuple(tuple(sublist) for sublist in trans)

histograma = {}

def add(trans, histograma):
    for item in trans:
        print(item)
        if item not in histograma:
            histograma[item] = 1
        else:
            histograma[item] += 1
   

for trans in transactions:
    add(trans, histograma)

for key, value in histograma.items():
    print(f"{key}: {value}")
