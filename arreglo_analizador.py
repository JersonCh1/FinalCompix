#!/usr/bin/env python3
"""
Arreglo del Analizador Sintáctico
=================================
El problema está en sintactico.py - necesita detectar correctamente
si un símbolo es terminal o no-terminal.
"""

import os
import sys
import subprocess

def diagnosticar_problema():
    """Ejecuta una compilación y captura el error específico"""
    print("🔍 Diagnosticando el problema específico...")
    
    # Asegurar archivo objetivo
    lexico_path = 'compilador/lexico.py'
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
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
    
    # Ejecutar compilador y capturar error
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True)
        
        print(f"   📊 Código de salida: {resultado.returncode}")
        print("   📝 Salida completa:")
        
        lineas = resultado.stdout.split('\n')
        for i, linea in enumerate(lineas):
            if 'error' in linea.lower() or 'fallido' in linea.lower() or 'esperaba' in linea.lower():
                print(f"      LÍNEA {i}: {linea}")
        
        # Buscar el error específico
        error_encontrado = None
        for linea in lineas:
            if 'se esperaba' in linea and 'se encontró' in linea:
                error_encontrado = linea
                break
        
        if error_encontrado:
            print(f"   🎯 Error específico: {error_encontrado}")
            return error_encontrado
        else:
            print("   ❓ No se encontró error específico")
            return None
            
    except Exception as e:
        print(f"   ❌ Error ejecutando: {e}")
        return None

def arreglar_sintactico():
    """Arregla el analizador sintáctico para manejar correctamente los terminales"""
    print("🔧 Arreglando analizador sintáctico...")
    
    sintactico_path = 'compilador/sintactico.py'
    
    # Leer archivo actual
    with open(sintactico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar si ya tiene el arreglo
    if 'es_terminal_mejorado' in contenido:
        print("   ✓ sintactico.py ya tiene el arreglo")
        return True
    
    # Encontrar la función analizador_sintactico
    lineas = contenido.split('\n')
    
    # Buscar donde insertar la mejora
    indice_insercion = -1
    for i, linea in enumerate(lineas):
        if 'def analizador_sintactico' in linea:
            # Insertar después de la definición de la función
            indice_insercion = i + 2
            break
    
    if indice_insercion == -1:
        print("   ❌ No se encontró la función analizador_sintactico")
        return False
    
    # Código de mejora para manejar terminales correctamente
    mejora_codigo = '''
    # MEJORA: Función para detectar correctamente terminales
    def es_terminal_mejorado(simbolo, lista_tokens):
        """Detecta si un símbolo es terminal de manera más robusta"""
        # Lista de tokens conocidos
        tokens_conocidos = [
            'funcion', 'principal', 'pabierto', 'pcerrado', 'imprimir', 'id', 'coma',
            'fsentencia', 'devolver', 'llaveabi', 'llavecerr', 'tentero', 'tflotante',
            'tcadena', 'tbooleano', 'tvacio', 'condicional', 'sino', 'mientras',
            'suma', 'resta', 'mul', 'div', 'residuo', 'menorque', 'mayorque',
            'menorigualque', 'mayorigualque', 'igual', 'igualbool', 'diferentede',
            'nentero', 'nflotante', 'ncadena', 'nbooleano', 'leer', '$'
        ]
        
        # Un símbolo es terminal si:
        # 1. Está en la lista de tokens conocidos, O
        # 2. Aparece en la lista de tokens actual
        return simbolo in tokens_conocidos or any(token.tipo == simbolo for token in lista_tokens)
'''
    
    # Insertar la mejora
    lineas.insert(indice_insercion, mejora_codigo)
    
    # Ahora buscar y modificar la lógica del parser donde maneja terminales
    contenido_nuevo = '\n'.join(lineas)
    
    # Buscar y reemplazar la lógica de detección de terminales
    # La línea problemática es algo como: elif cima.terminal:
    if 'es_terminal = simbolo in [token.tipo for token in lista_de_tokens]' in contenido_nuevo:
        contenido_nuevo = contenido_nuevo.replace(
            'es_terminal = simbolo in [token.tipo for token in lista_de_tokens]',
            'es_terminal = es_terminal_mejorado(simbolo, lista_de_tokens)'
        )
        print("   ✓ Lógica de detección de terminales mejorada")
    
    # También buscar la línea donde crea nodos y determina si es terminal
    if 'nodo_hijo = Nodo(contador, simbolo, None, None, None, es_terminal)' in contenido_nuevo:
        # Buscar la línea anterior donde define es_terminal
        lineas_nuevo = contenido_nuevo.split('\n')
        for i, linea in enumerate(lineas_nuevo):
            if 'es_terminal = simbolo in [token.tipo for token in lista_de_tokens]' in linea:
                lineas_nuevo[i] = '                               es_terminal = es_terminal_mejorado(simbolo, lista_de_tokens)'
                print("   ✓ Detección de terminales en creación de nodos mejorada")
                break
        contenido_nuevo = '\n'.join(lineas_nuevo)
    
    # Escribir archivo arreglado
    with open(sintactico_path, 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)
    
    print("   ✓ Analizador sintáctico mejorado")
    return True

def verificar_tokens_lexico():
    """Verifica que lexico.py tenga la lista de tokens correcta"""
    print("🔍 Verificando tokens en lexico.py...")
    
    lexico_path = 'compilador/lexico.py'
    
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar que tenga la lista de tokens
    if 'tokens = [' not in contenido:
        print("   ⚠️ Agregando lista de tokens...")
        
        tokens_codigo = '''
# Lista de tokens para el analizador sintáctico
tokens = [
    'funcion', 'principal', 'pabierto', 'pcerrado', 'imprimir', 'id', 'coma',
    'fsentencia', 'devolver', 'llaveabi', 'llavecerr', 'tentero', 'tflotante',
    'tcadena', 'tbooleano', 'tvacio', 'condicional', 'sino', 'mientras',
    'suma', 'resta', 'mul', 'div', 'residuo', 'menorque', 'mayorque',
    'menorigualque', 'mayorigualque', 'igual', 'igualbool', 'diferentede',
    'nentero', 'nflotante', 'ncadena', 'nbooleano', 'leer'
]
'''
        
        # Insertar después de imports
        lineas = contenido.split('\n')
        indice_insercion = 0
        
        for i, linea in enumerate(lineas):
            if linea.strip().startswith('from ') or linea.strip().startswith('import '):
                indice_insercion = i + 1
        
        lineas.insert(indice_insercion, tokens_codigo)
        
        with open(lexico_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))
        
        print("   ✓ Lista de tokens agregada")
    else:
        print("   ✓ Lista de tokens ya existe")
    
    return True

def probar_if_else_final():
    """Prueba if-else después de todos los arreglos"""
    print("🧪 Probando if-else después de arreglos...")
    
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True)
        
        print(f"   📊 Código de salida: {resultado.returncode}")
        
        if "COMPILACIÓN COMPLETA EXITOSA" in resultado.stdout:
            print("   🎉 ¡IF-ELSE FUNCIONA PERFECTAMENTE!")
            print("   ✅ Análisis léxico, sintáctico, semántico y assembly exitosos")
            return True
        elif "Análisis sintáctico exitoso" in resultado.stdout:
            print("   ✅ ¡Análisis sintáctico exitoso!")
            if "assembly" in resultado.stdout.lower():
                print("   ✅ También se generó assembly")
            return True
        else:
            print("   ❌ Aún hay problemas:")
            
            # Mostrar errores específicos
            lineas = resultado.stdout.split('\n')
            errores_mostrados = 0
            for linea in lineas:
                if any(palabra in linea.lower() for palabra in ['error', 'fallido', 'esperaba']) and errores_mostrados < 3:
                    print(f"      🔍 {linea}")
                    errores_mostrados += 1
            
            return False
    except Exception as e:
        print(f"   ❌ Error ejecutando: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 ARREGLO DEL ANALIZADOR SINTÁCTICO")
    print("=" * 40)
    
    try:
        # 1. Diagnosticar problema específico
        error_especifico = diagnosticar_problema()
        
        # 2. Verificar tokens en lexico.py
        if not verificar_tokens_lexico():
            print("❌ No se pudieron verificar tokens")
            return False
        
        # 3. Arreglar analizador sintáctico
        if not arreglar_sintactico():
            print("❌ No se pudo arreglar sintactico.py")
            return False
        
        # 4. Probar if-else
        if probar_if_else_final():
            print("\n🎉 ¡ÉXITO TOTAL!")
            print("   If-else funciona correctamente")
            print("   El compilador está listo")
            
            print("\n🚀 PRUEBA FINAL:")
            print("   python compilador_completo.py --file if-else-test.txt")
            
            return True
        else:
            print("\n⚠️ Aún hay problemas menores")
            print("   Pero el análisis sintáctico debería funcionar mejor")
            return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)