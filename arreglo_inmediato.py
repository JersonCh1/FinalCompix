#!/usr/bin/env python3
"""
Arreglo Inmediato para If-Else
==============================
Este script arregla específicamente el problema de if-else
reemplazando la gramática con la versión correcta.
"""

import os
import sys
import subprocess

def arreglar_gramatica_if_else():
    """Arregla la gramática específicamente para if-else"""
    print("🔧 Arreglando gramática para if-else...")
    
    # Gramática corregida - LA DIFERENCIA CLAVE ES LA REGLA CONDICIONAL
    gramatica_correcta = """programaprincipal -> funcion opcionprincipal masfuncn

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

# CORRECCION CRITICA: usar 'condicional' token, no no-terminal
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

    # Escribir gramática corregida
    with open('gramatica/gramatica.txt', 'w', encoding='utf-8') as f:
        f.write(gramatica_correcta)
    
    print("   ✓ Gramática corregida guardada")
    return True

def agregar_tokens_lexico():
    """Agrega la lista de tokens a lexico.py si no existe"""
    print("🔧 Verificando tokens en lexico.py...")
    
    lexico_path = 'compilador/lexico.py'
    
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar si ya tiene tokens
    if 'tokens = [' in contenido:
        print("   ✓ Tokens ya existen en lexico.py")
        return True
    
    # Agregar tokens después de imports
    tokens_code = '''
# Lista de tokens para el generador LL(1)
tokens = [
    'funcion', 'principal', 'pabierto', 'pcerrado', 'imprimir', 'comillas', 'id', 'coma', 
    'fsentencia', 'devolver', 'detener', 'llaveabi', 'llavecerr', 'tentero', 'tflotante', 
    'tbooleano', 'tcadena', 'tvacio', 'si', 'y', 'o', 'sino', 'entonces', 'mientras', 
    'para', 'suma', 'resta', 'mul', 'div', 'residuo', 'menorque', 'mayorque', 
    'menorigualque', 'mayorigualque', 'igual', 'igualbool', 'diferentede', 'nentero', 
    'nflotante', 'ncadena', 'nbooleano', 'leer', 'condicional'
]
'''
    
    # Insertar después de imports
    lineas = contenido.split('\n')
    indice_insercion = 0
    
    for i, linea in enumerate(lineas):
        if linea.strip().startswith('from ') or linea.strip().startswith('import '):
            indice_insercion = i + 1
    
    lineas.insert(indice_insercion, tokens_code)
    
    # Escribir archivo actualizado
    with open(lexico_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    
    print("   ✓ Tokens agregados a lexico.py")
    return True

def regenerar_tabla_ll1():
    """Regenera la tabla LL(1)"""
    print("🔄 Regenerando tabla LL(1)...")
    
    try:
        resultado = subprocess.run([
            sys.executable, 'generador-de-tablas-ll1/generador-ll1.py'
        ], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("   ✓ Tabla LL(1) regenerada exitosamente")
            return True
        else:
            print(f"   ❌ Error: {resultado.stderr}")
            print(f"   Salida: {resultado.stdout}")
            return False
    except Exception as e:
        print(f"   ❌ Error ejecutando: {e}")
        return False

def probar_if_else():
    """Prueba if-else después del arreglo"""
    print("🧪 Probando if-else...")
    
    # Asegurar que el archivo objetivo es if-else-test.txt
    lexico_path = 'compilador/lexico.py'
    
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Cambiar archivo objetivo si es necesario
    if "archivo = 'if-else-test.txt'" not in contenido:
        contenido_nuevo = contenido.replace(
            "archivo = 'recursion-test.txt'",
            "archivo = 'if-else-test.txt'"
        ).replace(
            "archivo = 'tipos-validos.txt'",
            "archivo = 'if-else-test.txt'"
        )
        
        with open(lexico_path, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("   ✓ Archivo objetivo cambiado a if-else-test.txt")
    
    # Ejecutar compilador
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True)
        
        if "exitoso" in resultado.stdout and "COMPILACIÓN COMPLETA EXITOSA" in resultado.stdout:
            print("   ✅ IF-ELSE FUNCIONA CORRECTAMENTE!")
            return True
        elif "exitoso" in resultado.stdout:
            print("   ⚠️ Compilación parcial (léxico/sintáctico ok, falló después)")
            return False
        else:
            print("   ❌ If-else sigue fallando")
            print("   Error:")
            # Mostrar últimas líneas del error
            lineas = resultado.stdout.split('\n')
            for linea in lineas[-10:]:
                if linea.strip():
                    print(f"      {linea}")
            return False
    except Exception as e:
        print(f"   ❌ Error ejecutando: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 ARREGLO INMEDIATO PARA IF-ELSE")
    print("=" * 35)
    
    try:
        # 1. Agregar tokens a lexico.py
        if not agregar_tokens_lexico():
            print("❌ No se pudieron agregar tokens")
            return False
        
        # 2. Arreglar gramática
        if not arreglar_gramatica_if_else():
            print("❌ No se pudo arreglar gramática")
            return False
        
        # 3. Regenerar tabla LL(1)
        if not regenerar_tabla_ll1():
            print("⚠️ No se pudo regenerar tabla LL(1)")
            print("   Continuando con tabla actual...")
        
        # 4. Probar if-else
        if probar_if_else():
            print("\n🎉 ¡ÉXITO! If-else funciona correctamente")
            print("   Ahora deberías poder compilar if-else-test.txt")
            return True
        else:
            print("\n⚠️ If-else aún tiene problemas")
            print("   Puede necesitar ajustes manuales en la tabla LL(1)")
            return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)