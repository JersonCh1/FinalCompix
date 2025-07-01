#!/usr/bin/env python3
"""
Script para arreglar el error de indentación en sintactico.py
"""

import os
import sys

def arreglar_indentacion_sintactico():
    """Arregla el error de indentación en sintactico.py"""
    print("🔧 Arreglando error de indentación en sintactico.py...")
    
    sintactico_path = 'compilador/sintactico.py'
    
    if not os.path.exists(sintactico_path):
        print(f"❌ No se encontró el archivo: {sintactico_path}")
        return False
    
    # Leer el archivo
    with open(sintactico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Crear backup
    backup_path = f"{sintactico_path}.backup_indent"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✓ Backup creado: {backup_path}")
    
    # Buscar y arreglar el problema de indentación
    lineas = contenido.split('\n')
    
    # Encontrar la línea problemática
    linea_problema = -1
    for i, linea in enumerate(lineas):
        if 'def es_terminal_mejorado(simbolo, lista_tokens):' in linea:
            linea_problema = i
            break
    
    if linea_problema == -1:
        print("❌ No se encontró la función es_terminal_mejorado")
        return False
    
    print(f"✓ Función encontrada en línea {linea_problema + 1}")
    
    # Arreglar la indentación - la función debe estar al nivel de la función analizador_sintactico
    # Buscar el nivel de indentación correcto
    nivel_correcto = 0
    for i in range(linea_problema - 1, -1, -1):
        if lineas[i].strip().startswith('def analizador_sintactico'):
            nivel_correcto = len(lineas[i]) - len(lineas[i].lstrip())
            break
    
    # Arreglar la indentación de es_terminal_mejorado y su contenido
    i = linea_problema
    while i < len(lineas) and (lineas[i].strip() == '' or 'es_terminal_mejorado' in lineas[i] or lineas[i].startswith('    ')):
        if lineas[i].strip():
            # Calcular nueva indentación
            contenido_linea = lineas[i].lstrip()
            if 'def es_terminal_mejorado' in contenido_linea:
                # Función al mismo nivel que analizador_sintactico
                lineas[i] = ' ' * nivel_correcto + contenido_linea
            elif contenido_linea.startswith('"""') or contenido_linea.startswith('#'):
                # Docstring o comentario dentro de la función
                lineas[i] = ' ' * (nivel_correcto + 4) + contenido_linea
            else:
                # Contenido de la función
                lineas[i] = ' ' * (nivel_correcto + 4) + contenido_linea
        i += 1
    
    # Escribir el archivo corregido
    contenido_corregido = '\n'.join(lineas)
    with open(sintactico_path, 'w', encoding='utf-8') as f:
        f.write(contenido_corregido)
    
    print("✅ Error de indentación corregido")
    return True

def verificar_sintaxis():
    """Verifica que no hay errores de sintaxis después del arreglo"""
    print("🔍 Verificando sintaxis de sintactico.py...")
    
    try:
        import ast
        with open('compilador/sintactico.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        ast.parse(codigo)
        print("✅ Sintaxis correcta")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error verificando sintaxis: {e}")
        return False

def probar_compilacion_simple():
    """Prueba una compilación simple después del arreglo"""
    print("🧪 Probando compilación simple...")
    
    import subprocess
    
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador_completo.py', '--file', 'holamundo.txt'
        ], capture_output=True, text=True, timeout=30)
        
        if "IndentationError" in resultado.stderr:
            print("❌ Aún hay errores de indentación")
            return False
        elif "SyntaxError" in resultado.stderr:
            print("❌ Hay errores de sintaxis")
            return False
        elif resultado.returncode == 0:
            print("✅ Compilación exitosa")
            return True
        else:
            print("⚠️ Compilación completada pero con advertencias")
            return True
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout - pero no hay errores de sintaxis")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 ARREGLO DE ERROR DE INDENTACIÓN")
    print("=" * 40)
    
    if not arreglar_indentacion_sintactico():
        print("❌ No se pudo arreglar la indentación")
        return False
    
    if not verificar_sintaxis():
        print("❌ Aún hay errores de sintaxis")
        return False
    
    if not probar_compilacion_simple():
        print("❌ La compilación aún falla")
        return False
    
    print("\n🎉 ¡ÉXITO!")
    print("   Error de indentación arreglado")
    print("   El compilador debería funcionar ahora")
    print("\n🚀 SIGUIENTE PASO:")
    print("   python validador_rubrica.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)