import tkinter as tk
from tkinter import messagebox
import ast
import operator

# Safe operator map
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg
}

def evaluate_expr(expr):
    try:
        tree = ast.parse(expr, mode='eval')
        return eval_node(tree.body)
    except Exception as e:
        return f"Error: {e}"

def eval_node(node):
    if isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        op_type = type(node.op)
        return operators[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = eval_node(node.operand)
        return operators[type(node.op)](operand)
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Constant):  # For Python 3.8+
        return node.value
    else:
        raise ValueError("Unsupported expression")

# GUI setup
def on_click(value):
    entry.insert(tk.END, value)

def clear():
    entry.delete(0, tk.END)

def calculate():
    expr = entry.get()
    result = evaluate_expr(expr)
    entry.delete(0, tk.END)
    entry.insert(0, result)

root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("400x560")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 24), bd=10, relief=tk.RIDGE, justify='right')
entry.pack(pady=20, fill=tk.X, padx=10)

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '%', '+'],
    ['(', ')', '**', 'C'],
    ['=']
]

frame = tk.Frame(root)
frame.pack()

for row in buttons:
    row_frame = tk.Frame(frame)
    row_frame.pack(expand=True, fill='both')
    for btn in row:
        action = lambda x=btn: on_click(x)
        if btn == '=':
            tk.Button(row_frame, text=btn, font=("Arial", 18), height=2, width=28, bg="#4CAF50", fg="white", command=calculate).pack(padx=1, pady=1)
        elif btn == 'C':
            tk.Button(row_frame, text=btn, font=("Arial", 18), height=2, width=6, bg="#f44336", fg="white", command=clear).pack(side=tk.LEFT, padx=1, pady=1)
        else:
            tk.Button(row_frame, text=btn, font=("Arial", 18), height=2, width=6, command=action).pack(side=tk.LEFT, padx=1, pady=1)

root.mainloop()
