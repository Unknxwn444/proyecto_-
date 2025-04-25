import pyodbc
import tkinter as tk
from tkinter import messagebox, simpledialog

# Configuración de la conexión a la base de datos
server = 'DESKTOP-KEIFM9N\\SQLEXPRESS'
database = 'DBProductosTienda'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID=HWH;PWD=compu*2025;'

try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa a SQL Server")
except Exception as e:
    print("Error al conectar:", e)
    exit()

# Funciones
def listar_categorias():
    try:
        cursor = conn.cursor()
        query = "SELECT Id, Nombre FROM Categorias"
        cursor.execute(query)
        categorias = cursor.fetchall()
        cursor.close()

        categorias_str = "\n".join([f"ID: {row.Id}, Nombre: {row.Nombre}" for row in categorias])
        messagebox.showinfo("Lista de Categorías", categorias_str if categorias_str else "No hay categorías.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron listar las categorías: {e}")

def listar_productos():
    try:
        cursor = conn.cursor()
        query = """
        SELECT p.Id, p.Nombre, p.Precio, p.Cantidad, c.Nombre AS Categoria, p.FechaRegistro
        FROM Productos p
        JOIN Categorias c ON p.CategoriaId = c.Id
        """
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()

        productos_str = "\n".join([
            f"ID: {row.Id}, Nombre: {row.Nombre}, Precio: {row.Precio}, Cantidad: {row.Cantidad}, "
            f"Categoría: {row.Categoria}, Registro: {row.FechaRegistro}" for row in productos
        ])
        messagebox.showinfo("Lista de Productos", productos_str if productos_str else "No hay productos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron listar los productos: {e}")

def insertar_producto():
    nombre = simpledialog.askstring("Nuevo Producto", "Ingrese el nombre del producto:")
    precio = simpledialog.askfloat("Nuevo Producto", "Ingrese el precio del producto:")
    cantidad = simpledialog.askinteger("Nuevo Producto", "Ingrese la cantidad del producto:")
    categoria_id = simpledialog.askinteger("Nuevo Producto", "Ingrese el ID de la categoría:")

    if nombre and precio is not None and cantidad is not None and categoria_id is not None:
        if precio < 0:
            messagebox.showerror("Error", "El precio no puede ser negativo.")
            return
        if cantidad < 0:
            messagebox.showerror("Error", "La cantidad no puede ser negativa.")
            return

        try:
            cursor = conn.cursor()
            query = "INSERT INTO Productos (Nombre, Precio, Cantidad, CategoriaId) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (nombre, precio, cantidad, categoria_id))
            conn.commit()
            cursor.close()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' insertado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

def actualizar_producto():
    id_producto = simpledialog.askinteger("Actualizar Producto", "Ingrese el ID del producto a actualizar:")
    nueva_cantidad = simpledialog.askinteger("Actualizar Producto", "Ingrese la nueva cantidad del producto:")

    if nueva_cantidad is not None and nueva_cantidad < 0:
        messagebox.showerror("Error", "La cantidad no puede ser negativa.")
        return

    try:
        cursor = conn.cursor()
        query = "UPDATE Productos SET Cantidad = ? WHERE Id = ?"
        cursor.execute(query, (nueva_cantidad, id_producto))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Éxito", f"Producto con ID {id_producto} actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar el producto: {e}")

def eliminar_producto():
    id_producto = simpledialog.askinteger("Eliminar Producto", "Ingrese el ID del producto a eliminar:")

    try:
        cursor = conn.cursor()
        query = "DELETE FROM Productos WHERE Id = ?"
        cursor.execute(query, (id_producto,))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar el producto: {e}")

# Interfaz Gráfica
root = tk.Tk()
root.title("Gestión de Productos")
root.geometry("400x300")
root.config(bg="#e0f7fa")

tk.Label(root, text="Sistema de Gestión de Productos", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=10)

tk.Button(root, text="Listar Categorías", command=listar_categorias, width=25).pack(pady=5)
tk.Button(root, text="Listar Productos", command=listar_productos, width=25).pack(pady=5)
tk.Button(root, text="Insertar Producto", command=insertar_producto, width=25).pack(pady=5)
tk.Button(root, text="Actualizar Producto", command=actualizar_producto, width=25).pack(pady=5)
tk.Button(root, text="Eliminar Producto", command=eliminar_producto, width=25).pack(pady=5)

tk.Button(root, text="Salir", command=root.destroy, bg="red", fg="white", width=25).pack(pady=15)

root.mainloop()
