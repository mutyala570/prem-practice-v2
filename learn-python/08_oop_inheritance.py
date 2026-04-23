"""
==============================================================
08 - OOP: Inheritance, super(), dunder methods, @property
==============================================================

CONCEPT:
- Inheritance: `class Child(Parent):`
- `super().__init__()` calls parent constructor
- Dunder methods (like __str__, __eq__) let you customize behavior
- @property makes a method look like an attribute
"""

# ---------------- EXAMPLE 1: Inheritance ----------------
print("=== Example 1: Inheritance ===")

class Animal:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def speak(self) -> str:
        return "Some sound"

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, species="Dog")    # call parent
        self.breed = breed

    def speak(self) -> str:       # override
        return "Woof!"


class Cat(Animal):
    def __init__(self, name: str):
        super().__init__(name, species="Cat")

    def speak(self) -> str:
        return "Meow!"


dog = Dog("Rex", "Labrador")
cat = Cat("Whiskers")

print(dog)                # Rex (Dog) — uses __str__
print(f"{dog.name} says {dog.speak()}")
print(f"{cat.name} says {cat.speak()}")


# ---------------- EXAMPLE 2: @property + dunder methods ----------------
print("\n=== Example 2: Property & Dunder Methods ===")

class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Computed attribute — no () needed when accessing."""
        return (self._celsius * 9 / 5) + 32

    # Dunder methods
    def __str__(self) -> str:
        return f"{self._celsius}°C"

    def __repr__(self) -> str:
        return f"Temperature(celsius={self._celsius})"

    def __eq__(self, other) -> bool:
        return self._celsius == other._celsius

    def __lt__(self, other) -> bool:
        return self._celsius < other._celsius


t1 = Temperature(25)
t2 = Temperature(25)
t3 = Temperature(30)

print(t1)                         # Uses __str__: 25°C
print(repr(t1))                   # Uses __repr__: Temperature(celsius=25)
print(f"In Fahrenheit: {t1.fahrenheit}")   # Access as attribute, not method
print(f"t1 == t2: {t1 == t2}")   # Uses __eq__
print(f"t1 < t3: {t1 < t3}")     # Uses __lt__

t1.celsius = 30        # setter
print(f"Updated: {t1}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Create `Vehicle` parent and `Car`, `Bike` children
# 2. Make a `Money` class with __add__ to allow Money(10) + Money(20)
# 3. Create `User` class with @property for full_name (first + last)
