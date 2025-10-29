import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ecommerce"
    )



def agregar_producto(nombre, descripcion, precio, stock):
    db = conectar()
    cursor = db.cursor()
    sql = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nombre, descripcion, precio, stock))
    db.commit()
    db.close()
    messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado.")
    mostrar_productos()

def mostrar_productos():
    for item in tree.get_children():
        tree.delete(item)
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM productos")
    for producto in cursor.fetchall():
        tree.insert("", "end", values=producto)
    db.close()

def actualizar_producto():
    try:
        selected = tree.selection()[0]
        id_producto = tree.item(selected)["values"][0]

        nombre = entry_nombre.get()
        descripcion = entry_descripcion.get()
        precio = entry_precio.get()
        stock = entry_stock.get()

        db = conectar()
        cursor = db.cursor()

        sql = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s"
        cursor.execute(sql, (nombre, descripcion, float(precio), int(stock), id_producto))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", "Producto actualizado.")
        mostrar_productos()
    except IndexError:
        messagebox.showwarning("Error", "Selecciona un producto para actualizar.")

def eliminar_producto():
    try:
        selected = tree.selection()[0]
        id_producto = tree.item(selected)["values"][0]

        db = conectar()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", (id_producto,))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", "Producto eliminado.")
        mostrar_productos()
    except IndexError:
        messagebox.showwarning("Error", "Selecciona un producto para eliminar.")

def llenar_campos(event):
    try:
        selected = tree.selection()[0]
        values = tree.item(selected)["values"]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, values[1])
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, values[2])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, values[3])
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, values[4])
    except IndexError:
        pass


root = tk.Tk()
root.title("CRUD E-commerce")
root.geometry("700x500")


tk.Label(root, text="Nom").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Descripción").grid(row=1, column=0, padx=5, pady=5)
entry_descripcion = tk.Entry(root)
entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Precio").grid(row=2, column=0, padx=5, pady=5)
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Stock").grid(row=3, column=0, padx=5, pady=5)
entry_stock = tk.Entry(root)
entry_stock.grid(row=3, column=1, padx=5, pady=5)

# Botones
tk.Button(root, text="Agregar", command=lambda: agregar_producto(
    entry_nombre.get(), entry_descripcion.get(), float(entry_precio.get()), int(entry_stock.get())
)).grid(row=4, column=0, pady=10)

tk.Button(root, text="Actualizar", command=actualizar_producto).grid(row=4, column=1, pady=10)
tk.Button(root, text="Eliminar", command=eliminar_producto).grid(row=4, column=2, pady=10)
tk.Button(root, text="Refrescar", command=mostrar_productos).grid(row=4, column=3, pady=10)

# Tabla de productos
columns = ("ID", "Nombre", "Descripción", "Precio", "Stock")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.bind("<<TreeviewSelect>>", llenar_campos)
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

# Ajustar el tamaño de las columnas
tree.column("ID", width=50)
tree.column("Nombre", width=150)
tree.column("Descripción", width=200)
tree.column("Precio", width=80)
tree.column("Stock", width=80)

mostrar_productos()
root.mainloop()
