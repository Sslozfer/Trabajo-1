import importlib
import sys

def mostrar_menu():
    print("\n🌍 Visualizador de Terremotos USGS 🌋")
    print("1. Ejecutar con pandas (recomendado)")
    print("2. Ejecutar sin pandas")
    print("3. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-3): ")
        
        if opcion == "1":
            try:
                importlib.import_module("con_pandas")
            except ImportError:
                print("❌ Error: pandas no esta instalado. Ejecuta 'pip install pandas' o usa la opción 2.")
        elif opcion == "2":
            importlib.import_module("sin_pandas")
        elif opcion == "3":
            print("¡Hasta luego! 👋")
            sys.exit()
        else:
            print("Opcion invalida. Intente de nuevo.")

if __name__ == "__main__":
    main()