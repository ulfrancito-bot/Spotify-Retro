# ...existing code...
import time

class COLOR:
    RED = '\x1b[0;31m'
    BOLD_RED = '\x1b[1;31m'
    NORMAL = '\x1b[0m'

def cargar_corazon():
    # Intentar archivos comunes, si no existen usar patrón embebido
    filenames = ['heart_pattern.txt', 'heart_pathern.txt', 'heart.txt']
    for fn in filenames:
        try:
            with open(fn, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            continue

    # Fallback: patrón con '@' para reemplazar letras
    return (
        "  @@@   @@@  \n"
        " @@@@@ @@@@@ \n"
        "@@@@@@@@@@@@@\n"
        "@@@@@@@@@@@@@\n"
        " @@@@@@@@@@@ \n"
        "  @@@@@@@@@  \n"
        "   @@@@@@@   \n"
        "    @@@@@    \n"
        "     @@@     \n"
        "      @      "
    )

def romantizar(nombre):
    corazon = cargar_corazon()
    letras = list(nombre)
    i = 0
    while '@' in corazon:
        corazon = corazon.replace('@', letras[i % len(letras)], 1)
        i += 1
    return corazon

def main():
    nombre = input("Nombre de la victima: ").strip() or "Cat Eyes"
    corazon = romantizar(nombre)

    print(f"\n{COLOR.BOLD_RED} Formando corazon para... {COLOR.NORMAL}\n")

    for linea in corazon.split('\n'):
        if linea.strip():
            print(f"{COLOR.RED}{linea}{COLOR.NORMAL}")
            time.sleep(0.3)

    print(f"\n{COLOR.BOLD_RED} Corazon formado! {COLOR.NORMAL}\n")

if __name__ == "__main__":
    main()
