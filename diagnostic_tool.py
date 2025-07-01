#!/usr/bin/env python3
"""
Herramienta de Diagnóstico para el Analizador Sintáctico
========================================================
Identifica exactamente qué está fallando en el compilador
"""

import os
import sys
import subprocess

def diagnosticar_archivo_especifico(archivo):
    """Diagnóstica un archivo específico con detalles"""
    print(f"\n🔍 DIAGNÓSTICO DETALLADO: {archivo}")
    print("=" * 50)
    
    # Modificar archivo objetivo
    lexico_path = 'compilador/lexico.py'
    with open(lexico_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Cambiar archivo objetivo
    lineas = contenido.split('\n')
    for i, linea in enumerate(lineas):
        if linea.strip().startswith("archivo = "):
            lineas[i] = f"archivo = '{archivo}'"
            break
    
    with open(lexico_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    
    # Ejecutar compilador con captura detallada
    try:
        resultado = subprocess.run([
            sys.executable, 'compilador/sintactico.py'
        ], capture_output=True, text=True, timeout=10)
        
        print(f"📊 Código de salida: {resultado.returncode}")
        print("\n📝 SALIDA COMPLETA:")
        print("-" * 40)
        print(resultado.stdout)
        print("-" * 40)
        
        if resultado.stderr:
            print("\n❌ ERRORES:")
            print("-" * 40)
            print(resultado.stderr)
            print("-" * 40)
        
        # Analizar la salida
        analizar_salida(resultado.stdout, resultado.stderr)
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - El compilador se colgó")
    except Exception as e:
        print(f"💥 ERROR EJECUTANDO: {e}")

def analizar_salida(stdout, stderr):
    """Analiza la salida para identificar problemas específicos"""
    print("\n🔬 ANÁLISIS DE RESULTADOS:")
    
    # Verificar etapas completadas
    etapas = {
        'Léxico': 'Analisis lexico exitoso' in stdout,
        'Tokens guardados': 'Tokens escritos exitosamente' in stdout,
        'Sintáctico': 'Análisis sintáctico exitoso' in stdout,
        'Árbol generado': '.dot creado en:' in stdout,
        'Tabla símbolos': 'Tabla de símbolos generada' in stdout,
        'Semántico': 'Verificación semántica exitosa' in stdout,
        'Tipos': 'Verificación de tipos exitosa' in stdout,
        'Assembly': 'assembly generado exitosamente' in stdout
    }
    
    for etapa, completada in etapas.items():
        status = "✅" if completada else "❌"
        print(f"   {status} {etapa}")
    
    # Buscar errores específicos
    if 'Error sintáctico' in stdout:
        print("\n🚨 ERROR SINTÁCTICO DETECTADO:")
        lineas = stdout.split('\n')
        for linea in lineas:
            if 'Error' in linea or 'error' in linea:
                print(f"   {linea}")
    
    if 'se esperaba' in stdout:
        print("\n🎯 PROBLEMA DE PARSING:")
        lineas = stdout.split('\n')
        for linea in lineas:
            if 'se esperaba' in linea:
                print(f"   {linea}")
    
    # Verificar archivos generados
    verificar_archivos_generados()

def verificar_archivos_generados():
    """Verifica qué archivos se generaron"""
    print("\n📁 ARCHIVOS GENERADOS:")
    
    directorios = [
        ('salida-tokens', '*.txt'),
        ('salida-arboles', '*.dot'),
        ('salida-arboles', '*.csv'),
        ('salida-assembly', '*.s'),
        ('salida-assembly-mips', '*.asm')
    ]
    
    import glob
    from pathlib import Path
    
    for directorio, patron in directorios:
        if os.path.exists(directorio):
            archivos = list(Path(directorio).glob(patron))
            if archivos:
                print(f"   ✅ {directorio}: {len(archivos)} archivos")
                for archivo in archivos[-2:]:  # Mostrar últimos 2
                    print(f"      - {archivo.name}")
            else:
                print(f"   ❌ {directorio}: sin archivos")
        else:
            print(f"   ❌ {directorio}: directorio no existe")

def probar_tabla_ll1():
    """Verifica que la tabla LL(1) esté correcta"""
    print("\n🔍 VERIFICANDO TABLA LL(1):")
    
    tabla_path = 'tabla-ll1/tabla_ll1.csv'
    if not os.path.exists(tabla_path):
        print("❌ Tabla LL(1) no existe")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(tabla_path, index_col=0)
        
        print(f"   ✅ Tabla cargada: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        # Verificar entradas críticas
        entradas_criticas = [
            ('masinstrucciones', 'condicional'),
            ('instruccion', 'condicional'),
            ('condicional', 'condicional'),
            ('masinstrucciones', 'funcion'),
            ('programaprincipal', 'funcion')
        ]
        
        for fila, columna in entradas_criticas:
            if fila in df.index and columna in df.columns:
                valor = df.at[fila, columna]
                if pd.isna(valor) or valor.strip() == '':
                    print(f"   ❌ {fila} + {columna}: VACÍO")
                else:
                    print(f"   ✅ {fila} + {columna}: '{valor}'")
            else:
                print(f"   ❌ {fila} + {columna}: NO EXISTE")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando tabla: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔬 HERRAMIENTA DE DIAGNÓSTICO SINTÁCTICO")
    print("=" * 45)
    
    # Verificar tabla LL(1) primero
    probar_tabla_ll1()
    
    # Diagnosticar archivos específicos
    archivos_prueba = [
        'holamundo.txt',        # Más simple
        'tipos-validos.txt',    # Expresiones básicas
        'if-else-test.txt',     # If-else
        'recursion-test.txt'    # Funciones
    ]
    
    for archivo in archivos_prueba:
        if os.path.exists(f'codigos-bocetos/{archivo}'):
            diagnosticar_archivo_especifico(archivo)
        else:
            print(f"\n❌ Archivo no encontrado: {archivo}")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print("1. Revisa los errores sintácticos específicos arriba")
    print("2. Verifica que la tabla LL(1) tenga las entradas necesarias")
    print("3. Si hay problemas de parsing, revisa la gramática")
    print("4. Si no se genera assembly, revisa el módulo assembly_mips.py")

if __name__ == "__main__":
    main()