##Codigo sola input siempre tengo que pensar que hay un menu

def menu():
    print("Bienvenide al menu de sus productos favoritos:")
    print("1. Ingrese su producto favorito")
    print("2.Ver su lista de productos")
    print("3.Salir del menu")
    
def ingresar_productos(lista):
    productos=input("Ingrese producto:"). strip() #Para espacios en blanco si no ingresa nada
    if productos:
        lista.append(productos)
        print(f"Producto {productos} ingresado")
    else:
        print(f"Producto no ingresado")
