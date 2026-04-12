import os

# just to make sure we are in the right directory, you can ignore this line if you are running this code in an IDE like PyCharm or Jupyter Notebook,
# because they will automatically set the working directory to the project directory.

os.chdir(os.path.dirname(os.path.dirname(__file__))) 

class Fruit:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
    def describe(self):
        return f"{self.name} is {self.color}"


# put this all inside main
if __name__ == "__main__":
    apple = Fruit("Apple", "Red")
    print(apple.describe())


    # write into json file
    import json
    fruit_dict = {"name": apple.name, "color": apple.color}
    with open("avoid/fruit.json", "w") as f: # here the "w" means write mode, if the file does not exist, it will be created, if it exists, it will be overwritten
        json.dump(fruit_dict, f)


    # read from json file
    with open("avoid/fruit.json", "r") as f: # here the "r" means read mode
        data = json.load(f)
        print(data)

    # this is a huge problem, because we are losing the methods of the class, we can only get the attributes,
    # but we cannot use the describe method anymore.
    # This is a common issue when working with json files, we need to find a way to preserve the methods of the class when we save it to a json file.


    # and now here is the role of pickle, which is a python module that allows us to serialize and deserialize python objects, including the methods of the class.