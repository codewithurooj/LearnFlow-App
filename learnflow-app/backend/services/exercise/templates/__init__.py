"""
Exercise Templates

Pre-defined exercise templates for different topics and difficulty levels.
"""

BEGINNER_TEMPLATES = {
    "variables": {
        "title": "Variable Assignment",
        "description": """# Variable Assignment

Create variables to store:
1. Your name as a string
2. Your age as an integer
3. Whether you like Python as a boolean

Print all three variables.
""",
        "starter_code": """# Create your variables here
name = ""
age = 0
likes_python = False

# Print them
print(name, age, likes_python)
""",
        "test_cases": [
            {"input": "", "expected_output": "", "hidden": False},
        ],
    },
    "strings": {
        "title": "String Manipulation",
        "description": """# String Manipulation

Write a function that takes a name and returns a greeting.

Example:
- Input: "Alice"
- Output: "Hello, Alice!"
""",
        "starter_code": """def greet(name):
    # TODO: Return a greeting with the name
    pass

# Test your function
print(greet("Alice"))
""",
        "test_cases": [
            {"input": "", "expected_output": "Hello, Alice!", "hidden": False},
            {"input": "", "expected_output": "Hello, Bob!", "hidden": True},
        ],
    },
}

LEARNING_TEMPLATES = {
    "functions": {
        "title": "Function with Multiple Parameters",
        "description": """# Calculate Area

Write a function that calculates the area of a rectangle.

Parameters:
- width: The width of the rectangle
- height: The height of the rectangle

Return the area (width * height).
""",
        "starter_code": """def calculate_area(width, height):
    # TODO: Calculate and return the area
    pass

# Test
print(calculate_area(5, 3))  # Should print 15
""",
        "test_cases": [
            {"input": "", "expected_output": "15", "hidden": False},
            {"input": "", "expected_output": "0", "hidden": True},
        ],
    },
}

PROFICIENT_TEMPLATES = {
    "classes": {
        "title": "Create a Class",
        "description": """# Student Class

Create a Student class with:
- `__init__` that takes name and grades (list of numbers)
- `average` method that returns the average grade
- `is_passing` method that returns True if average >= 60
""",
        "starter_code": """class Student:
    def __init__(self, name, grades):
        # TODO: Initialize attributes
        pass

    def average(self):
        # TODO: Return average grade
        pass

    def is_passing(self):
        # TODO: Return True if passing
        pass

# Test
s = Student("Alice", [80, 90, 70])
print(s.average())
print(s.is_passing())
""",
        "test_cases": [
            {"input": "", "expected_output": "80.0\nTrue", "hidden": False},
        ],
    },
}


def get_template(topic: str, difficulty: str) -> dict | None:
    """Get a template for a topic and difficulty."""
    templates = {
        "beginner": BEGINNER_TEMPLATES,
        "learning": LEARNING_TEMPLATES,
        "proficient": PROFICIENT_TEMPLATES,
    }

    level_templates = templates.get(difficulty.lower(), BEGINNER_TEMPLATES)
    return level_templates.get(topic.lower())
