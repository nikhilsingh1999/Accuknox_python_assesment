class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        """
        This makes the Rectangle class iterable.
        It uses the 'yield' keyword to return one item at a time.
        """
        yield {'length': self.length}
        yield {'width': self.width}


# Example usage:
if __name__ == "__main__":
    rect = Rectangle(10, 5)

    # Iterate using for loop
    for item in rect:
        print(item)

    # Or convert to list
    print(list(rect))
