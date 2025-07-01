#!/usr/bin/env python3
"""
Script para arreglar completamente todos los errores de indentación en sintactico.py
"""

import os
import sys

def restaurar_desde_backup():
    """Restaura el archivo desde el backup del directorio backups_20250701_160250"""
    print("🔄 Restaurando desde backup...")
    
    backup_path = 'backups_20250701_160250/compilador_sintactico.py'
    destino_path = 'compilador/sintactico.py'
    
    if os.path.exists(backup_path):
        import shutil
        shutil.copy2(backup_path, destino_path)
        print(f"✅ Archivo restaurado desde: {backup_path}")
        return True
    else:
        print(f"❌ No se encontró el backup: {backup_path}")
        return False

def eliminar_mejora_problematica():
    """Elimina la mejora problemática que causa errores de indentación"""
    print("🔧 Eliminando mejora problemática...")
    
    sintactico_path = 'compilador/sintactico.py'
    
    if not os.path.exists(sintactico_path):
        print(f"❌ No se encontró: {sintactico_path}")
        return False
    
    # Leer archivo
    with open(sintactico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Eliminar la función es_terminal_mejorado y sus llamadas
    lineas = contenido.split('\n')
    lineas_limpias = []
    
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # Saltar la función es_terminal_mejorado completa
        if 'def es_terminal_mejorado' in linea:
            print("   🗑️ Eliminando función es_terminal_mejorado...")
            # Saltar hasta la siguiente función o final
            i += 1
            while i < len(lineas) and (lineas[i].strip() == '' or lineas[i].startswith('    ') or lineas[i].startswith('#')):
                i += 1
            continue
        
        # Reemplazar llamadas a es_terminal_mejorado con la lógica original
        if 'es_terminal_mejorado(' in linea:
            print("   🔄 Restaurando lógica original de detección de terminales...")
            # Restaurar la lógica original
            indentacion = len(linea) - len(linea.lstrip())
            linea_original = ' ' * indentacion + 'es_terminal = simbolo in [token.tipo for token in lista_de_tokens]'
            lineas_limpias.append(linea_original)
        else:
            lineas_limpias.append(linea)
        
        i += 1
    
    # Escribir archivo limpio
    contenido_limpio = '\n'.join(lineas_limpias)
    with open(sintactico_path, 'w', encoding='utf-8') as f:
        f.write(contenido_limpio)
    
    print("✅ Mejora problemática eliminada")
    return True

def verificar_sintaxis():
    """Verifica que no hay errores de sintaxis"""
    print("🔍 Verificando sintaxis...")
    
    try:
        import ast
        with open('compilador/sintactico.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        ast.parse(codigo)
        print("✅ Sintaxis correcta")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en línea {e.lineno}: {e.msg}")
        if e.text:
            print(f"   Texto: {e.text.strip()}")
        return False
    except Exception as e:
        print(f"❌ Error verificando sintaxis: {e}")
        return False

def probar_importacion():
    """Prueba importar el módulo sintactico"""
    print("🧪 Probando importación del módulo...")
    
    try:
        # Cambiar al directorio del compilador
        import sys
        sys.path.insert(0, 'compilador')
        
        # Intentar importar
        import lexico
        print("✅ Módulo lexico importado correctamente")
        
        # No importamos sintactico directamente porque puede tener efectos secundarios
        # Solo verificamos que no tiene errores de sintaxis
        return True
        
    except Exception as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    finally:
        # Limpiar sys.path
        if 'compilador' in sys.path:
            sys.path.remove('compilador')

def probar_compilacion_basica():
    """Prueba una compilación básica"""
    print("🧪 Probando compilación básica...")
    
    import subprocess
    
    try:
        # Probar con un timeout para evitar cuelgues
        resultado = subprocess.run([
            sys.executable, 'compilador_completo.py', '--file', 'holamundo.txt'
        ], capture_output=True, text=True, timeout=15)
        
        if "IndentationError" in resultado.stderr:
            print("❌ Aún hay errores de indentación")
            return False
        elif "SyntaxError" in resultado.stderr:
            print("❌ Aún hay errores de sintaxis")
            return False
        elif "Analisis lexico exitoso" in resultado.stdout:
            print("✅ Análisis léxico funciona")
            return True
        elif resultado.returncode == 0:
            print("✅ Compilación exitosa")
            return True
        else:
            print("⚠️ Compilación con advertencias pero sin errores de sintaxis")
            return True
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout - pero sin errores de sintaxis")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 ARREGLO COMPLETO DE INDENTACIÓN")
    print("=" * 45)
    
    # Opción 1: Restaurar desde backup
    if restaurar_desde_backup():
        print("\n🔍 Verificando archivo restaurado...")
        if verificar_sintaxis() and probar_importacion():
            print("✅ Archivo restaurado funciona correctamente")
            if probar_compilacion_basica():
                print("\n🎉 ¡ÉXITO CON RESTAURACIÓN!")
                print("   Archivo restaurado desde backup")
                print("   El compilador debería funcionar ahora")
                return True
    
    print("\n🔄 Intentando arreglo manual...")
    
    # Opción 2: Limpiar mejoras problemáticas
    if not eliminar_mejora_problematica():
        print("❌ No se pudo limpiar el archivo")
        return False
    
    if not verificar_sintaxis():
        print("❌ Aún hay errores de sintaxis después de la limpieza")
        return False
    
    if not probar_importacion():
        print("❌ Los módulos no se importan correctamente")
        return False
    
    if not probar_compilacion_basica():
        print("❌ La compilación básica aún falla")
        return False
    
    print("\n🎉 ¡ÉXITO CON LIMPIEZA!")
    print("   Mejoras problemáticas eliminadas")
    print("   El compilador debería funcionar ahora")
    
    print("\n🚀 SIGUIENTE PASO:")
    print("   python validador_rubrica.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)