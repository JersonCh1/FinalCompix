#!/usr/bin/env python3
"""
Validador de Rúbrica - Compilador Completo
==========================================

Este script valida que el compilador cumple con todos los requisitos de la rúbrica:

1. Analizador Léxico y Sintáctico (2 puntos)
2. Analizador Semántico (4 puntos) 
3. Generación Expresiones Aritméticas (3 puntos)
4. Generación If-Else (5 puntos)
5. Generación Funciones (5 puntos)

Total: 19 puntos
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

class ValidadorRubrica:
    def __init__(self):
        self.resultados = {
            'timestamp': datetime.now().isoformat(),
            'puntuacion_total': 0,
            'puntuacion_maxima': 19,
            'criterios': {},
            'archivos_probados': [],
            'errores_encontrados': []
        }
        
        # Definir criterios de evaluación
        self.criterios = {
            'lexico_sintactico': {
                'puntos': 2,
                'descripcion': 'Analizador Léxico y Sintáctico',
                'archivos_prueba': ['holamundo.txt', 'tipos-validos.txt'],
                'requisitos': [
                    'Análisis léxico exitoso',
                    'Árbol sintáctico generado',
                    'Tokens correctos'
                ]
            },
            'semantico': {
                'puntos': 4,
                'descripcion': 'Analizador Semántico',
                'archivos_prueba': ['tipos-validos.txt', 'verificarvariable.txt'],
                'requisitos': [
                    'Tabla de símbolos',
                    'Verificación de variables',
                    'Verificación de tipos'
                ]
            },
            'expresiones': {
                'puntos': 3,
                'descripcion': 'Generación Expresiones Aritméticas',
                'archivos_prueba': ['sumanumeros.txt', 'tipos-validos.txt'],
                'requisitos': [
                    'Operaciones básicas (+, -, *, /)',
                    'Código assembly generado',
                    'SPIM compatible'
                ]
            },
            'if_else': {
                'puntos': 5,
                'descripcion': 'Generación If-Else',
                'archivos_prueba': ['if-else-test.txt'],
                'requisitos': [
                    'Análisis sintáctico correcto',
                    'Código assembly generado',
                    'Estructuras condicionales funcionales'
                ]
            },
            'funciones': {
                'puntos': 5,
                'descripcion': 'Generación Funciones',
                'archivos_prueba': ['recursion-test.txt', 'fibonaccirecursivo.txt'],
                'requisitos': [
                    'Definición de funciones',
                    'Llamadas de funciones',
                    'Recursividad funcional'
                ]
            }
        }
    
    def modificar_archivo_objetivo(self, nombre_archivo):
        """Modifica el archivo objetivo en lexico.py"""
        lexico_path = Path('compilador/lexico.py')
        
        if not lexico_path.exists():
            return False
        
        with open(lexico_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        lineas = contenido.split('\n')
        for i, linea in enumerate(lineas):
            if linea.strip().startswith("archivo = "):
                lineas[i] = f"archivo = '{nombre_archivo}'"
                break
        
        with open(lexico_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))
        
        return True
    
    def ejecutar_compilador(self, archivo):
        """Ejecuta el compilador con un archivo específico"""
        try:
            if not self.modificar_archivo_objetivo(archivo):
                return None, "No se pudo modificar archivo objetivo"
            
            inicio = time.time()
            resultado = subprocess.run([
                sys.executable, 'compilador/sintactico.py'
            ], capture_output=True, text=True, cwd='.')
            tiempo = time.time() - inicio
            
            info = {
                'archivo': archivo,
                'tiempo': round(tiempo, 3),
                'codigo_salida': resultado.returncode,
                'stdout': resultado.stdout,
                'stderr': resultado.stderr,
                'exitoso': resultado.returncode == 0
            }
            
            return info, None
            
        except Exception as e:
            return None, str(e)
    
    def validar_lexico_sintactico(self):
        """Valida analizador léxico y sintáctico (2 puntos)"""
        print("🔍 Validando Analizador Léxico y Sintáctico...")
        
        criterio = self.criterios['lexico_sintactico']
        puntos_obtenidos = 0
        detalles = []
        
        for archivo in criterio['archivos_prueba']:
            print(f"   📄 Probando: {archivo}")
            
            info, error = self.ejecutar_compilador(archivo)
            
            if error:
                detalles.append(f"❌ Error con {archivo}: {error}")
                continue
            
            self.resultados['archivos_probados'].append(info)
            
            # Verificar análisis léxico
            if "Analisis lexico exitoso" in info['stdout']:
                detalles.append(f"✅ {archivo}: Análisis léxico exitoso")
                puntos_obtenidos += 0.5
            else:
                detalles.append(f"❌ {archivo}: Análisis léxico falló")
            
            # Verificar árbol sintáctico
            if "Análisis sintáctico exitoso" in info['stdout']:
                detalles.append(f"✅ {archivo}: Árbol sintáctico generado")
                puntos_obtenidos += 0.5
            else:
                detalles.append(f"❌ {archivo}: Análisis sintáctico falló")
            
            # Verificar tokens generados
            if "Tokens escritos exitosamente" in info['stdout']:
                detalles.append(f"✅ {archivo}: Tokens generados correctamente")
                puntos_obtenidos += 0.5
            else:
                detalles.append(f"❌ {archivo}: Tokens no generados")
        
        # Máximo 2 puntos
        puntos_obtenidos = min(puntos_obtenidos, 2)
        
        self.resultados['criterios']['lexico_sintactico'] = {
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_maximos': 2,
            'detalles': detalles,
            'estado': 'CUMPLE' if puntos_obtenidos >= 1.5 else 'NO CUMPLE'
        }
        
        print(f"   🎯 Puntuación: {puntos_obtenidos}/2")
        return puntos_obtenidos
    
    def validar_semantico(self):
        """Valida analizador semántico (4 puntos)"""
        print("🔍 Validando Analizador Semántico...")
        
        criterio = self.criterios['semantico']
        puntos_obtenidos = 0
        detalles = []
        
        for archivo in criterio['archivos_prueba']:
            print(f"   📄 Probando: {archivo}")
            
            info, error = self.ejecutar_compilador(archivo)
            
            if error:
                detalles.append(f"❌ Error con {archivo}: {error}")
                continue
            
            # Verificar tabla de símbolos
            if "Tabla de símbolos generada" in info['stdout']:
                detalles.append(f"✅ {archivo}: Tabla de símbolos generada")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Tabla de símbolos no generada")
            
            # Verificar verificación semántica
            if "Verificación semántica exitosa" in info['stdout']:
                detalles.append(f"✅ {archivo}: Verificación semántica exitosa")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Verificación semántica falló")
            
            # Verificar verificación de tipos
            if "Verificación de tipos exitosa" in info['stdout']:
                detalles.append(f"✅ {archivo}: Verificación de tipos exitosa")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Verificación de tipos falló")
        
        # Máximo 4 puntos
        puntos_obtenidos = min(puntos_obtenidos, 4)
        
        self.resultados['criterios']['semantico'] = {
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_maximos': 4,
            'detalles': detalles,
            'estado': 'CUMPLE' if puntos_obtenidos >= 3 else 'NO CUMPLE'
        }
        
        print(f"   🎯 Puntuación: {puntos_obtenidos}/4")
        return puntos_obtenidos
    
    def validar_expresiones(self):
        """Valida generación de expresiones aritméticas (3 puntos)"""
        print("🔍 Validando Generación de Expresiones...")
        
        criterio = self.criterios['expresiones']
        puntos_obtenidos = 0
        detalles = []
        
        for archivo in criterio['archivos_prueba']:
            print(f"   📄 Probando: {archivo}")
            
            info, error = self.ejecutar_compilador(archivo)
            
            if error:
                detalles.append(f"❌ Error con {archivo}: {error}")
                continue
            
            # Verificar generación de assembly
            if "Código assembly MIPS generado exitosamente" in info['stdout']:
                detalles.append(f"✅ {archivo}: Assembly MIPS generado")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Assembly MIPS no generado")
            
            # Verificar compatibilidad SPIM
            if "SPIM simulator" in info['stdout']:
                detalles.append(f"✅ {archivo}: Compatible con SPIM")
                puntos_obtenidos += 0.5
            else:
                detalles.append(f"❌ {archivo}: No menciona compatibilidad SPIM")
        
        # Verificar archivos de salida
        if os.path.exists('salida-assembly-mips'):
            archivos_asm = list(Path('salida-assembly-mips').glob('*.asm'))
            if archivos_asm:
                detalles.append(f"✅ Archivos assembly encontrados: {len(archivos_asm)}")
                puntos_obtenidos += 0.5
            else:
                detalles.append("❌ No se encontraron archivos assembly")
        
        # Máximo 3 puntos
        puntos_obtenidos = min(puntos_obtenidos, 3)
        
        self.resultados['criterios']['expresiones'] = {
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_maximos': 3,
            'detalles': detalles,
            'estado': 'CUMPLE' if puntos_obtenidos >= 2 else 'NO CUMPLE'
        }
        
        print(f"   🎯 Puntuación: {puntos_obtenidos}/3")
        return puntos_obtenidos
    
    def validar_if_else(self):
        """Valida generación de if-else (5 puntos)"""
        print("🔍 Validando Generación If-Else...")
        
        criterio = self.criterios['if_else']
        puntos_obtenidos = 0
        detalles = []
        
        for archivo in criterio['archivos_prueba']:
            print(f"   📄 Probando: {archivo}")
            
            info, error = self.ejecutar_compilador(archivo)
            
            if error:
                detalles.append(f"❌ Error con {archivo}: {error}")
                continue
            
            # Verificar análisis sintáctico
            if "Análisis sintáctico exitoso" in info['stdout']:
                detalles.append(f"✅ {archivo}: Análisis sintáctico exitoso")
                puntos_obtenidos += 2
            else:
                detalles.append(f"❌ {archivo}: Análisis sintáctico falló")
                if "Error sintáctico" in info['stdout']:
                    detalles.append("   ⚠️ Error en parsing de if-else")
            
            # Verificar generación de assembly
            if "Código assembly MIPS generado exitosamente" in info['stdout']:
                detalles.append(f"✅ {archivo}: Assembly con if-else generado")
                puntos_obtenidos += 2
            else:
                detalles.append(f"❌ {archivo}: Assembly con if-else no generado")
            
            # Verificar estructura condicional en assembly
            if puntos_obtenidos >= 2:
                # Buscar archivo assembly generado
                asm_path = f"salida-assembly-mips/{os.path.splitext(archivo)[0]}.asm"
                if os.path.exists(asm_path):
                    with open(asm_path, 'r') as f:
                        codigo_asm = f.read()
                    
                    # Buscar instrucciones de salto condicional
                    if any(instr in codigo_asm for instr in ['beq', 'bne', 'blt', 'bgt']):
                        detalles.append(f"✅ {archivo}: Instrucciones condicionales encontradas")
                        puntos_obtenidos += 1
                    else:
                        detalles.append(f"❌ {archivo}: No se encontraron instrucciones condicionales")
        
        # Máximo 5 puntos
        puntos_obtenidos = min(puntos_obtenidos, 5)
        
        self.resultados['criterios']['if_else'] = {
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_maximos': 5,
            'detalles': detalles,
            'estado': 'CUMPLE' if puntos_obtenidos >= 4 else 'NO CUMPLE'
        }
        
        print(f"   🎯 Puntuación: {puntos_obtenidos}/5")
        return puntos_obtenidos
    
    def validar_funciones(self):
        """Valida generación de funciones (5 puntos)"""
        print("🔍 Validando Generación de Funciones...")
        
        criterio = self.criterios['funciones']
        puntos_obtenidos = 0
        detalles = []
        
        for archivo in criterio['archivos_prueba']:
            print(f"   📄 Probando: {archivo}")
            
            info, error = self.ejecutar_compilador(archivo)
            
            if error:
                detalles.append(f"❌ Error con {archivo}: {error}")
                continue
            
            # Verificar análisis sintáctico de funciones
            if "Análisis sintáctico exitoso" in info['stdout']:
                detalles.append(f"✅ {archivo}: Análisis sintáctico exitoso")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Análisis sintáctico falló")
                continue
            
            # Verificar tabla de símbolos con funciones
            if "función" in info['stdout']:
                detalles.append(f"✅ {archivo}: Funciones en tabla de símbolos")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Funciones no registradas")
            
            # Verificar generación de assembly
            if "Código assembly MIPS generado exitosamente" in info['stdout']:
                detalles.append(f"✅ {archivo}: Assembly con funciones generado")
                puntos_obtenidos += 1
            else:
                detalles.append(f"❌ {archivo}: Assembly con funciones no generado")
            
            # Verificar recursividad en assembly
            if puntos_obtenidos >= 3:
                asm_path = f"salida-assembly-mips/{os.path.splitext(archivo)[0]}.asm"
                if os.path.exists(asm_path):
                    with open(asm_path, 'r') as f:
                        codigo_asm = f.read()
                    
                    # Buscar instrucciones de llamada/retorno
                    if 'jal' in codigo_asm and 'jr $ra' in codigo_asm:
                        detalles.append(f"✅ {archivo}: Instrucciones de función encontradas")
                        puntos_obtenidos += 1
                    else:
                        detalles.append(f"❌ {archivo}: Instrucciones de función no encontradas")
                    
                    # Verificar recursividad específica
                    if archivo == 'recursion-test.txt' or archivo == 'fibonaccirecursivo.txt':
                        nombre_func = 'factorial' if 'factorial' in codigo_asm else 'fibonacci_recursivo'
                        if f'jal {nombre_func}' in codigo_asm:
                            detalles.append(f"✅ {archivo}: Recursividad implementada")
                            puntos_obtenidos += 1
                        else:
                            detalles.append(f"❌ {archivo}: Recursividad no implementada")
        
        # Máximo 5 puntos
        puntos_obtenidos = min(puntos_obtenidos, 5)
        
        self.resultados['criterios']['funciones'] = {
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_maximos': 5,
            'detalles': detalles,
            'estado': 'CUMPLE' if puntos_obtenidos >= 4 else 'NO CUMPLE'
        }
        
        print(f"   🎯 Puntuación: {puntos_obtenidos}/5")
        return puntos_obtenidos
    
    def verificar_estructura_proyecto(self):
        """Verifica que la estructura del proyecto sea correcta"""
        print("🔍 Verificando estructura del proyecto...")
        
        archivos_requeridos = [
            'compilador/lexico.py',
            'compilador/sintactico.py',
            'compilador/assembly_mips.py',
            'gramatica/gramatica.txt',
            'tabla-ll1/tabla_ll1.csv',
            'codigos-bocetos/if-else-test.txt',
            'codigos-bocetos/recursion-test.txt'
        ]
        
        archivos_faltantes = []
        for archivo in archivos_requeridos:
            if not os.path.exists(archivo):
                archivos_faltantes.append(archivo)
        
        if archivos_faltantes:
            print("   ❌ Archivos faltantes:")
            for archivo in archivos_faltantes:
                print(f"      - {archivo}")
            return False
        else:
            print("   ✅ Estructura del proyecto correcta")
            return True
    
    def generar_reporte(self):
        """Genera un reporte detallado de la validación"""
        # Calcular puntuación total
        self.resultados['puntuacion_total'] = sum(
            criterio['puntos_obtenidos'] 
            for criterio in self.resultados['criterios'].values()
        )
        
        # Calcular porcentaje
        porcentaje = (self.resultados['puntuacion_total'] / self.resultados['puntuacion_maxima']) * 100
        
        # Crear directorio de reportes
        os.makedirs('reportes', exist_ok=True)
        
        # Guardar reporte JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_reporte = f'reportes/validacion_rubrica_{timestamp}.json'
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        return archivo_reporte, porcentaje
    
    def mostrar_resumen(self, porcentaje):
        """Muestra un resumen de los resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VALIDACIÓN DE RÚBRICA")
        print("=" * 60)
        
        print(f"📈 Puntuación Total: {self.resultados['puntuacion_total']}/{self.resultados['puntuacion_maxima']} ({porcentaje:.1f}%)")
        print()
        
        # Mostrar cada criterio
        for nombre, criterio in self.resultados['criterios'].items():
            estado_icon = "✅" if criterio['estado'] == 'CUMPLE' else "❌"
            print(f"{estado_icon} {self.criterios[nombre]['descripcion']}: {criterio['puntos_obtenidos']}/{criterio['puntos_maximos']}")
            
            # Mostrar algunos detalles importantes
            for detalle in criterio['detalles'][:3]:  # Solo primeros 3
                print(f"   {detalle}")
            
            if len(criterio['detalles']) > 3:
                print(f"   ... y {len(criterio['detalles']) - 3} más")
            print()
        
        # Clasificación
        if porcentaje >= 90:
            clasificacion = "🏆 EXCELENTE"
        elif porcentaje >= 80:
            clasificacion = "🥇 MUY BUENO"
        elif porcentaje >= 70:
            clasificacion = "🥈 BUENO"
        elif porcentaje >= 60:
            clasificacion = "🥉 SATISFACTORIO"
        else:
            clasificacion = "📝 NECESITA MEJORAS"
        
        print(f"🎯 Clasificación: {clasificacion}")
        
        # Recomendaciones
        print("\n📋 RECOMENDACIONES:")
        
        criterios_fallidos = [
            nombre for nombre, criterio in self.resultados['criterios'].items()
            if criterio['estado'] == 'NO CUMPLE'
        ]
        
        if not criterios_fallidos:
            print("   🎉 ¡Felicitaciones! Todos los criterios están cumplidos.")
        else:
            print("   📌 Criterios que necesitan atención:")
            for criterio in criterios_fallidos:
                print(f"      - {self.criterios[criterio]['descripcion']}")
                print(f"        Puntos faltantes: {self.criterios[criterio]['puntos'] - self.resultados['criterios'][criterio]['puntos_obtenidos']}")
    
    def ejecutar_validacion_completa(self):
        """Ejecuta la validación completa de la rúbrica"""
        print("🎯 VALIDADOR DE RÚBRICA - COMPILADOR COMPLETO")
        print("=" * 50)
        
        # Verificar estructura
        if not self.verificar_estructura_proyecto():
            print("❌ Estructura del proyecto incorrecta. Abortando validación.")
            return False
        
        print()
        
        # Ejecutar validaciones
        puntos_lexico = self.validar_lexico_sintactico()
        print()
        
        puntos_semantico = self.validar_semantico()
        print()
        
        puntos_expresiones = self.validar_expresiones()
        print()
        
        puntos_if_else = self.validar_if_else()
        print()
        
        puntos_funciones = self.validar_funciones()
        print()
        
        # Generar reporte
        archivo_reporte, porcentaje = self.generar_reporte()
        
        # Mostrar resumen
        self.mostrar_resumen(porcentaje)
        
        print(f"\n📄 Reporte detallado guardado en: {archivo_reporte}")
        
        return porcentaje >= 70  # 70% o más para aprobar

def main():
    """Función principal"""
    try:
        validador = ValidadorRubrica()
        exito = validador.ejecutar_validacion_completa()
        
        if exito:
            print("\n✅ VALIDACIÓN EXITOSA - El compilador cumple con la rúbrica")
            return 0
        else:
            print("\n❌ VALIDACIÓN FALLIDA - El compilador necesita mejoras")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Validación interrumpida por el usuario")
        return 130
    except Exception as e:
        print(f"\n💥 Error durante la validación: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())