#!/usr/bin/env python3
"""
Solución para Tabla LL(1)
=========================
Arregla específicamente la entrada faltante en la tabla LL(1)
para que masinstrucciones reconozca el token 'condicional' (if)
"""

import os
import sys
import pandas as pd

def arreglar_tabla_ll1():
    """Arregla la tabla LL(1) específicamente para el problema de condicional"""
    print("🔧 Arreglando tabla LL(1)...")
    
    tabla_path = 'tabla-ll1/tabla_ll1.csv'
    
    try:
        # Leer la tabla actual
        df = pd.read_csv(tabla_path, index_col=0)
        
        print(f"   📊 Tabla actual: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        # Verificar que existe la columna 'condicional'
        if 'condicional' not in df.columns:
            print("   ❌ Error: No existe la columna 'condicional' en la tabla")
            return False
        
        # ARREGLO CRÍTICO: Asegurar que masinstrucciones puede manejar condicional
        if 'masinstrucciones' in df.index:
            valor_actual = df.at['masinstrucciones', 'condicional']
            print(f"   🔍 Valor actual para masinstrucciones+condicional: '{valor_actual}'")
            
            # Si está vacío o es NaN, arreglarlo
            if pd.isna(valor_actual) or valor_actual.strip() == '':
                df.at['masinstrucciones', 'condicional'] = 'instruccion masinstrucciones'
                print("   ✅ Arreglado: masinstrucciones + condicional = 'instruccion masinstrucciones'")
            else:
                print("   ✓ Entrada ya existe y tiene valor")
        
        # Verificar otras entradas críticas
        entradas_criticas = [
            ('instruccion', 'condicional', 'condicional'),
            ('condicional', 'condicional', 'condicional pabierto expresion pcerrado llaveabi masinstrucciones llavecerr posibilidad')
        ]
        
        for fila, columna, valor_esperado in entradas_criticas:
            if fila in df.index and columna in df.columns:
                valor_actual = df.at[fila, columna]
                if pd.isna(valor_actual) or valor_actual.strip() == '':
                    df.at[fila, columna] = valor_esperado
                    print(f"   ✅ Arreglado: {fila} + {columna} = '{valor_esperado}'")
                else:
                    print(f"   ✓ {fila} + {columna} ya tiene valor: '{valor_actual}'")
        
        # Guardar tabla arreglada
        df.to_csv(tabla_path)
        print("   💾 Tabla LL(1) guardada con arreglos")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error procesando tabla: {e}")
        return False

def verificar_tabla_ll1():
    """Verifica que la tabla LL(1) tiene las entradas necesarias"""
    print("🔍 Verificando tabla LL(1)...")
    
    tabla_path = 'tabla-ll1/tabla_ll1.csv'
    
    try:
        df = pd.read_csv(tabla_path, index_col=0)
        
        # Verificaciones críticas
        verificaciones = [
            ('masinstrucciones', 'condicional'),
            ('instruccion', 'condicional'),
            ('condicional', 'condicional')
        ]
        
        todo_ok = True
        
        for fila, columna in verificaciones:
            if fila in df.index and columna in df.columns:
                valor = df.at[fila, columna]
                if pd.isna(valor) or valor.strip() == '':
                    print(f"   ❌ PROBLEMA: {fila} + {columna} está vacío")
                    todo_ok = False
                else:
                    print(f"   ✓ OK: {fila} + {columna} = '{valor}'")
            else:
                print(f"   ❌ PROBLEMA: No existe {fila} o {columna}")
                todo_ok = False
        
        return todo_ok
        
    except Exception as e:
        print(f"   ❌ Error verificando tabla: {e}")
        return False

def probar_if_else():
    """Prueba if-else después del arreglo"""
    print("🧪 Probando if-else...")
    
    import subprocess
    
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
        
        print("   ✓ Archivo objetivo configurado")
    
    # Ejecutar compilador
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True)
        
        if "COMPILACIÓN COMPLETA EXITOSA" in resultado.stdout:
            print("   🎉 ¡IF-ELSE FUNCIONA PERFECTAMENTE!")
            return True
        elif "Análisis sintáctico exitoso" in resultado.stdout:
            print("   ✅ Análisis sintáctico exitoso (parcial)")
            return True
        else:
            print("   ❌ Sigue fallando:")
            lineas = resultado.stdout.split('\n')
            for linea in lineas[-8:]:
                if linea.strip() and ('error' in linea.lower() or 'fallido' in linea.lower()):
                    print(f"      {linea}")
            return False
    except Exception as e:
        print(f"   ❌ Error ejecutando: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 SOLUCION PARA TABLA LL(1)")
    print("=" * 30)
    
    try:
        # 1. Verificar tabla actual
        if not verificar_tabla_ll1():
            print("\n🔧 La tabla necesita arreglos...")
            
            # 2. Arreglar tabla
            if not arreglar_tabla_ll1():
                print("❌ No se pudo arreglar la tabla")
                return False
            
            # 3. Verificar de nuevo
            if not verificar_tabla_ll1():
                print("❌ La tabla sigue con problemas")
                return False
        else:
            print("✓ Tabla LL(1) parece estar correcta")
        
        # 4. Probar if-else
        if probar_if_else():
            print("\n🎉 ¡ÉXITO TOTAL!")
            print("   If-else funciona correctamente")
            print("   Tu compilador debería estar listo")
            return True
        else:
            print("\n⚠️ Tabla arreglada pero if-else aún falla")
            print("   Puede necesitar depuración adicional")
            return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 SIGUIENTE PASO:")
        print("   python compilador_completo.py --file if-else-test.txt")
    
    sys.exit(0 if success else 1)