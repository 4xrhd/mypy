def quadratic_solver(a, b, c):
    """Solves the quadratic equation ax^2 + bx + c = 0."""
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Check if the discriminant is positive, negative, or zero
    if discriminant > 0:
        # Two real and distinct roots
        root1 = (-b + (discriminant ** 0.5)) / (2*a)
        root2 = (-b - (discriminant ** 0.5)) / (2*a)
        return root1, root2
    elif discriminant == 0:
        # One real root (repeated)
        root = -b / (2*a)
        return root, root
    else:
        # Complex roots
        real_part = -b / (2*a)
        imag_part = (abs(discriminant) ** 0.5) / (2*a)
        return complex(real_part, imag_part), complex(real_part, -imag_part)

# Take input from the user
a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))
c = int(input("Enter value of c: "))

# Solve the quadratic equation
root1, root2 = quadratic_solver(a, b, c)

# Display the roots
print("Root 1:", root1)
print("Root 2:", root2)
