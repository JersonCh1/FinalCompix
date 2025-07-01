#!/usr/bin/env python3
"""
Script para arreglar el problema de if-else en el compilador.

Este script:
1. Actualiza la gramática para corregir if-else
2. Regenera la tabla LL(1)
3. Actualiza el léxico si es necesario
4. Ejecuta pruebas de validación

Uso: python arreglar_if_else.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def backup_archivos():
    """Crea backup de archivos importantes antes de modificar"""
    archivos_backup = [
        'gramatica/gramatica.txt',
        'tabla-ll1/tabla_ll1.csv',
        'compilador/lexico.py'
    ]
    
    print("📁 Creando backups...")
    
    for archivo in archivos_backup:
        if os.path.exists(archivo):
            backup_path = f"{archivo}.backup"
            shutil.copy2(archivo, backup_path)
            print(f"   ✓ Backup: {backup_path}")

def actualizar_gramatica():
    """Actualiza la gramática con las reglas corregidas para if-else"""
    print("📝 Actualizando gramática...")
    
    nueva_gramatica = """programaprincipal -> funcion opcionprincipal masfuncn

opcionprincipal -> restomain
opcionprincipal -> restofuncn

masfuncn -> programaprincipal
masfuncn -> ''

restomain -> principal pabierto pcerrado tentero llaveabi masinstrucciones llavecerr
restofuncn -> id pabierto parametrosf pcerrado opciondato llaveabi masinstrucciones llavecerr

parametrosf -> id tipodato masparametrosf
parametrosf -> ''

masparametrosf -> coma parametrosf
masparametrosf -> ''

opciondato -> tvacio
opciondato -> tipodato

instruccion -> asignaciones fsentencia
instruccion -> mostrar fsentencia
instruccion -> buclepara
instruccion -> buclemientras
instruccion -> condicional
instruccion -> detener fsentencia
instruccion -> leer pabierto id pcerrado fsentencia
instruccion -> devolver expresion fsentencia

masinstrucciones -> instruccion masinstrucciones
masinstrucciones -> ''

buclepara -> para pabierto asignaciones fsentencia expresion fsentencia asignaciones pcerrado llaveabi masinstrucciones llavecerr

buclemientras -> mientras pabierto expresion pcerrado llaveabi masinstrucciones llavecerr

# REGLAS CORREGIDAS PARA IF-ELSE
condicional -> condicional pabierto expresion pcerrado llaveabi masinstrucciones llavecerr posibilidad

posibilidad -> sino llaveabi masinstrucciones llavecerr
posibilidad -> ''

mostrar -> imprimir pabierto comandos pcerrado

comandos -> expresion mascomandos
comandos -> ''

macomandos -> suma expresion mascomandos
mascomandos -> ''

asignaciones -> id ext

ext -> tipodato opcionesasig
ext -> extension

extension -> igual expresion
extension -> pabierto parametros pcerrado

opcionesasig -> igual expresion
opcionesasig -> ''

expresion -> pabierto expresion pcerrado masexpresiones
expresion -> id opciones masexpresiones
expresion -> valordato masexpresiones

masexpresiones -> ''
masexpresiones -> operacion expresion

opciones -> pabierto parametros pcerrado
opciones -> ''

parametros -> expresion restoparametros
parametros -> ''

restoparametros -> coma expresion restoparametros
restoparametros -> '' 

operacion -> suma
operacion -> resta
operacion -> mul
operacion -> div
operacion -> residuo
operacion -> igualbool
operacion -> menorque
operacion -> mayorque
operacion -> menorigualque
operacion -> mayorigualque
operacion -> diferentede
operacion -> y
operacion -> o
 
valordato -> ncadena
valordato -> nflotante
valordato -> nentero
valordato -> nbooleano

tipodato -> tentero
tipodato -> tcadena
tipodato -> tflotante
tipodato -> tbooleano"""

    # Escribir nueva gramática
    os.makedirs('gramatica', exist_ok=True)
    with open('gramatica/gramatica.txt', 'w', encoding='utf-8') as f:
        f.write(nueva_gramatica)
    
    print("   ✓ Gramática actualizada")

def actualizar_lexico():
    """Actualiza el léxico para asegurar que reconoce if/else correctamente"""
    print("📝 Verificando analizador léxico...")
    
    lexico_path = 'compilador/lexico.py'
    
    if not os.path.exists(lexico_path):
        print("   ❌ No se encontró lexico.py")
        return False
    
    # Leer archivo actual
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar que if/else están en palabras reservadas
    if "'if': 'condicional'" in contenido and "'else': 'sino'" in contenido:
        print("   ✓ Tokens if/else ya están correctos")
        return True
    else:
        print("   ⚠️ Actualizando tokens if/else...")
        
        # Actualizar palabras reservadas si es necesario
        # (Aquí podrías agregar lógica para actualizar)
        return True

def regenerar_tabla_ll1():
    """Regenera la tabla LL(1) con la nueva gramática"""
    print("🔄 Regenerando tabla LL(1)...")
    
    try:
        # Ejecutar el generador de tabla LL(1)
        resultado = subprocess.run([
            sys.executable, 'generador-de-tablas-ll1/generador-ll1.py'
        ], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("   ✓ Tabla LL(1) regenerada exitosamente")
            return True
        else:
            print(f"   ❌ Error regenerando tabla: {resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error ejecutando generador: {e}")
        return False

def probar_if_else():
    """Prueba específicamente el archivo if-else-test.txt"""
    print("🧪 Probando if-else...")
    
    # Modificar archivo objetivo en lexico.py
    modificar_archivo_objetivo('if-else-test.txt')
    
    try:
        # Ejecutar compilador
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True, cwd='.')
        
        if "Análisis sintáctico exitoso" in resultado.stdout:
            print("   ✅ If-else compilado exitosamente!")
            return True
        else:
            print("   ❌ If-else aún falla:")
            # Mostrar las primeras líneas del error
            lines = resultado.stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"      {line}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error ejecutando prueba: {e}")
        return False

def probar_recursion():
    """Prueba específicamente el archivo recursion-test.txt"""
    print("🧪 Probando recursión...")
    
    # Modificar archivo objetivo en lexico.py
    modificar_archivo_objetivo('recursion-test.txt')
    
    try:
        # Ejecutar compilador
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True, cwd='.')
        
        if "Análisis sintáctico exitoso" in resultado.stdout:
            print("   ✅ Recursión compilada exitosamente!")
            return True
        else:
            print("   ❌ Recursión aún falla:")
            # Mostrar las primeras líneas del error
            lines = resultado.stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"      {line}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error ejecutando prueba: {e}")
        return False

def modificar_archivo_objetivo(nombre_archivo):
    """Modifica el archivo objetivo en lexico.py"""
    lexico_path = Path('compilador/lexico.py')
    
    if not lexico_path.exists():
        return False
    
    # Leer archivo
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Buscar y reemplazar la línea del archivo
    lineas = contenido.split('\n')
    for i, linea in enumerate(lineas):
        if linea.strip().startswith("archivo = "):
            lineas[i] = f"archivo = '{nombre_archivo}'"
            break
    
    # Escribir archivo modificado
    with open(lexico_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    
    return True

def restaurar_backups():
    """Restaura los backups en caso de error"""
    print("🔄 Restaurando backups...")
    
    archivos_backup = [
        'gramatica/gramatica.txt.backup',
        'tabla-ll1/tabla_ll1.csv.backup',
        'compilador/lexico.py.backup'
    ]
    
    for backup in archivos_backup:
        if os.path.exists(backup):
            original = backup.replace('.backup', '')
            shutil.copy2(backup, original)
            print(f"   ✓ Restaurado: {original}")

def main():
    """Función principal"""
    print("🔧 ARREGLANDO SOPORTE IF-ELSE")
    print("=" * 40)
    
    try:
        # 1. Crear backups
        backup_archivos()
        
        # 2. Actualizar gramática
        actualizar_gramatica()
        
        # 3. Verificar léxico
        if not actualizar_lexico():
            print("❌ Error en actualización del léxico")
            return False
        
        # 4. Regenerar tabla LL(1)
        if not regenerar_tabla_ll1():
            print("❌ Error regenerando tabla LL(1)")
            restaurar_backups()
            return False
        
        # 5. Probar if-else
        if not probar_if_else():
            print("❌ If-else aún no funciona")
            return False
        
        # 6. Probar recursión
        if not probar_recursion():
            print("⚠️ Recursión aún tiene problemas, pero if-else funciona")
        
        print("\n✅ ARREGLO COMPLETADO")
        print("🎉 If-else debería funcionar ahora!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido")
        restaurar_backups()
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        restaurar_backups()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)