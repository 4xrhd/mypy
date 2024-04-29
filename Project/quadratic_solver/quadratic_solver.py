from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the values of a, b, and c from the form
        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])
        
        # Calculate roots
        root1, root2 = quadratic_solver(a, b, c)
        
        # Render the template with the results
        return render_template("index.html", a=a, b=b, c=c, root1=root1, root2=root2)
    else:
        # Render the form template
        return render_template("index.html")

if __name__ == "__main__":
    # Open the browser automatically
    webbrowser.open("http://127.0.0.1:5000/")
    # Run the Flask app
    app.run(debug=True)
