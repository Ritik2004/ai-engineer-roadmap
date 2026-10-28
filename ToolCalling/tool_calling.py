requests = [
    {"name": "add", "args": {"a": 2, "b": 3}},
    {"name": "multiply", "args": {"a": 4, "b": 8}},
    {"name": "greet", "args": {"name": "Ritik"}},
    {"name": "divide", "args": {"a": 10, "b": 2}}
]

def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

def greet(name):
    return f"Hello: {name}"

tools = {"add":add, "multiply":multiply,"greet":greet}

for req in requests:
    if(req["name"] not in tools):
        print("Unknown tool:", req["name"])
        continue
    func = tools[req["name"]]
    print(func(**req["args"]))