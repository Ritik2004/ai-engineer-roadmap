
# list store values and allow duplicates
sample_list = [1,2,3,4,5]
sample_list.append(6)
sample_list.remove(3)
sample_list.sort()
sample_list.reverse()

# print(sample_list[0])
# print(sample_list[-1]);



# Tuples ordered and immutable
sample_tuple = (1,2,3,4,5)
# a single element requires a trailing comma
single_item_tuple = (1,)


# set unordered and unique
sample_set = {1,2,3,4,5}
sample_set.add(6)
sample_set.remove(3)
# print(sample_set)


# dictionaries key-values pairs
sample_dict = {"name": "John",
        "age": 30,
        "city":"Delhi",
        "skills":["Python", "Java", "C++"]
        }
# print(sample_dict["name"])
# print(sample_dict["skills"])
sample_dict["city"] = "Mumbai"

# for key,value in sample_dict.items():
#     print(key, value)


# loops and conditions

score = 75

# if score >= 90 and score <= 100:
#     print("Grade A")
# elif score >= 60:
#     print("Grade B")
# else:
#     print("Grade C")


# loops
# for i in range(1,6):
#     print(i)

# sample_list = [1,2,3,4,5]
# for i in sample_list:
#     print(i)

# for index,value in enumerate(sample_list):
#     print(index, value)

def add(a, b):
    return a + b

# result = add(5, 10)
# print("The sum is:", result)


def multiply(a,b=3):
    return a * b

# mult_result = multiply(5)
# print("The multiplication result is:", mult_result)

# *args use it when we dont know how many arguments will be passed

def total(*args):
    return sum(args)

# print(total(1,2,3,4,5))  

# **kwargs** use it when we dont know how many keyword arguments will be passed
def print1(**kwargs):
    for key,value in kwargs.items():
        print(key, value)
# print1(name="John", age=30, city="Delhi")

# num = [1,2,2,3,4,5,5]
# print(list(set(num))) 

# words = ['ai','python','ai','ml','python']
# ans={}

# for word in words:
#     if word in ans:
#         ans[word]+=1
#     else:
#         ans[word]=1;

# print(ans)

# list1=[];
# for i in range(1,21):
#     if i%2==0:
#         list1.append(i)
# print(list1)

# def func1(*args):
#     return sum(args)

# print(func1(1,2,3,4,5)) 



# def func2(**kwargs):
#     return kwargs;

# print(func2(name="John", age=30, city="Delhi"))  

salary={"amit":"100",
        "rahul":"50",
        "raj":"200"
        }

# def get_salary(item):
#     return int(item[1])

# # ans = dict((sorted(salary.items(),key=get_salary)))
# ans = dict(sorted(salary.items(), key=lambda x : int(x[1])))
# print(ans)



