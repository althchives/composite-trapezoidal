from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def composite_trapezoidal(f_str, a, b, n):
    """
    Composite Trapezoidal Rule implementation
    
    Parameters:
    f_str: string representation of function
    a: lower bound
    b: upper bound
    n: number of subintervals
    
    Returns:
    result: approximate integral value
    steps: list of calculation steps for display
    """
    try:
        # Parse the function
        f = lambda x: eval(f_str.replace('^', '**'))
        
        # Calculate step size
        h = (b - a) / n
        
        # Initialize steps for display
        steps = []
        steps.append(f"Step 1: Calculate step size h = (b - a) / n = ({b} - {a}) / {n} = {h}")
        
        # Calculate f(x0) and f(xn)
        f_a = f(a)
        f_b = f(b)
        steps.append(f"Step 2: Calculate f(a) = f({a}) = {f_a}")
        steps.append(f"Step 3: Calculate f(b) = f({b}) = {f_b}")
        
        # Calculate sum of interior points
        sum_interior = 0
        interior_values = []
        for i in range(1, n):
            x_i = a + i * h
            f_xi = f(x_i)
            sum_interior += f_xi
            interior_values.append(f"f({x_i:.6f}) = {f_xi:.6f}")
        
        steps.append(f"Step 4: Calculate interior points:")
        for val in interior_values:
            steps.append(f"  {val}")
        steps.append(f"  Sum of interior points = {sum_interior}")
        
        # Apply trapezoidal formula
        result = (h / 2) * (f_a + 2 * sum_interior + f_b)
        
        steps.append(f"Step 5: Apply formula: I ≈ (h/2)[f(a) + 2∑f(xi) + f(b)]")
        steps.append(f"  I ≈ ({h}/2)[{f_a} + 2({sum_interior}) + {f_b}]")
        steps.append(f"  I ≈ ({h}/2)[{f_a + 2*sum_interior + f_b}]")
        steps.append(f"  I ≈ {result}")
        
        return result, steps
        
    except Exception as e:
        return None, [f"Error: {str(e)}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        f_str = data['function']
        a = float(data['a'])
        b = float(data['b'])
        n = int(data['n'])
        
        if n <= 0:
            return jsonify({'error': 'Number of subintervals must be positive'})
        
        result, steps = composite_trapezoidal(f_str, a, b, n)
        
        if result is None:
            return jsonify({'error': steps[0]})
        
        return jsonify({
            'result': result,
            'steps': steps
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()