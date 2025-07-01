import os

def buscar_hijo(nodo, tipo):
    """Encuentra un hijo con el tipo especificado."""
    for hijo in nodo.hijos:
        if hijo.tipo == tipo:
            return hijo
    return None

class GeneradorAssemblyMIPS:
    def __init__(self):
        self.codigo = []
        self.contador_etiquetas = 0
        self.contador_temporales = 0
        self.offset_variables = {}
        self.offset_actual = 0
        self.en_funcion = False
        self.funciones_declaradas = set()
        
    def nueva_etiqueta(self, prefijo="L"):
        """Genera una nueva etiqueta única"""
        self.contador_etiquetas += 1
        return f"{prefijo}{self.contador_etiquetas}"
    
    def nuevo_temporal(self):
        """Genera un nuevo registro temporal"""
        self.contador_temporales += 1
        return f"$t{(self.contador_temporales - 1) % 8}"
    
    def agregar_codigo(self, instruccion, comentario=""):
        """Agrega una línea de código MIPS"""
        if comentario:
            self.codigo.append(f"    {instruccion:<25} # {comentario}")
        else:
            self.codigo.append(f"    {instruccion}")
    
    def agregar_etiqueta(self, etiqueta):
        """Agrega una etiqueta"""
        self.codigo.append(f"{etiqueta}:")
    
    def generar_preambulo(self):
        """Genera el preámbulo del programa MIPS"""
        self.codigo.extend([
            "# Compilador completo - Código MIPS generado",
            "# Arquitectura: MIPS32",
            "# Simulador: SPIM",
            "",
            ".data",
            "    newline: .asciiz \"\\n\"",
            "    space: .asciiz \" \"",
            "",
            ".text",
            ".globl main",
            ""
        ])
    
    def obtener_offset_variable(self, nombre_var, ambito):
        """Obtiene el offset de una variable en el stack"""
        simbolo = ambito.buscar_simbolo(nombre_var)
        if not simbolo:
            return None
        
        if nombre_var not in self.offset_variables:
            self.offset_actual += 4  # 4 bytes por variable en MIPS
            self.offset_variables[nombre_var] = self.offset_actual
        
        return self.offset_variables[nombre_var]
    
    def generar_expresion(self, nodo_expresion, ambito, registro_destino="$t0"):
        """Genera código para una expresión y retorna el registro resultado"""
        if not nodo_expresion:
            return None
            
        if nodo_expresion.tipo == 'expresion':
            primer_hijo = nodo_expresion.hijos[0] if nodo_expresion.hijos else None
            
            if primer_hijo and primer_hijo.tipo == 'valordato':
                return self.generar_valor_dato(primer_hijo, registro_destino)
            
            elif primer_hijo and primer_hijo.tipo == 'id':
                nombre_var = primer_hijo.valor
                offset = self.obtener_offset_variable(nombre_var, ambito)
                
                if offset is not None:
                    self.agregar_codigo(f"lw {registro_destino}, -{offset}($fp)", f"cargar variable {nombre_var}")
                    
                    # Verificar si hay operaciones adicionales
                    masexpresiones = buscar_hijo(nodo_expresion, 'masexpresiones')
                    if masexpresiones and masexpresiones.hijos and masexpresiones.hijos[0].tipo != 'e':
                        return self.generar_operacion_binaria(registro_destino, masexpresiones, ambito)
                    
                    return registro_destino
                
            elif primer_hijo and primer_hijo.tipo == 'pabierto':
                # Expresión entre paréntesis
                expr_interna = buscar_hijo(nodo_expresion, 'expresion')
                if expr_interna:
                    return self.generar_expresion(expr_interna, ambito, registro_destino)
                    
        elif nodo_expresion.tipo == 'valordato':
            return self.generar_valor_dato(nodo_expresion, registro_destino)
            
        return None
    
    def generar_valor_dato(self, nodo_valordato, registro_destino="$t0"):
        """Genera código para un valor literal"""
        if not nodo_valordato.hijos:
            return None
            
        tipo_valor = nodo_valordato.hijos[0].tipo
        valor = nodo_valordato.hijos[0].valor
        
        if tipo_valor == 'nentero':
            self.agregar_codigo(f"li {registro_destino}, {valor}", f"cargar entero {valor}")
            return registro_destino
        elif tipo_valor == 'nflotante':
            # Para flotantes necesitaríamos registros $f
            # Por simplicidad, convertimos a entero * 100
            valor_int = int(float(valor) * 100)
            self.agregar_codigo(f"li {registro_destino}, {valor_int}", f"cargar float {valor} como entero * 100")
            return registro_destino
        elif tipo_valor == 'ncadena':
            # Para cadenas necesitaríamos manejo especial en la sección .data
            etiqueta_string = self.nueva_etiqueta("str")
            # Agregar a la sección .data (simplificado)
            self.agregar_codigo(f"la {registro_destino}, {etiqueta_string}", f"cargar dirección de cadena")
            return registro_destino
            
        return None
    
    def generar_operacion_binaria(self, registro_izq, nodo_masexpresiones, ambito):
        """Genera código para operaciones binarias"""
        if not nodo_masexpresiones or not nodo_masexpresiones.hijos:
            return registro_izq
            
        nodo_operacion = buscar_hijo(nodo_masexpresiones, 'operacion')
        nodo_expr_der = buscar_hijo(nodo_masexpresiones, 'expresion')
        
        if not nodo_operacion or not nodo_expr_der:
            return registro_izq
        
        # Generar el operando derecho
        registro_der = self.nuevo_temporal()
        self.generar_expresion(nodo_expr_der, ambito, registro_der)
        
        # Generar la operación
        tipo_op = nodo_operacion.hijos[0].tipo
        registro_resultado = self.nuevo_temporal()
        
        if tipo_op == 'suma':
            self.agregar_codigo(f"add {registro_resultado}, {registro_izq}, {registro_der}", "suma")
        elif tipo_op == 'resta':
            self.agregar_codigo(f"sub {registro_resultado}, {registro_izq}, {registro_der}", "resta")
        elif tipo_op == 'mul':
            self.agregar_codigo(f"mul {registro_resultado}, {registro_izq}, {registro_der}", "multiplicación")
        elif tipo_op == 'div':
            self.agregar_codigo(f"div {registro_izq}, {registro_der}", "división")
            self.agregar_codigo(f"mflo {registro_resultado}", "obtener resultado división")
        elif tipo_op == 'menorque':
            self.agregar_codigo(f"slt {registro_resultado}, {registro_izq}, {registro_der}", "comparar <")
        elif tipo_op == 'mayorque':
            self.agregar_codigo(f"sgt {registro_resultado}, {registro_izq}, {registro_der}", "comparar >")
        elif tipo_op == 'igualbool':
            self.agregar_codigo(f"seq {registro_resultado}, {registro_izq}, {registro_der}", "comparar ==")
        elif tipo_op == 'diferentede':
            self.agregar_codigo(f"sne {registro_resultado}, {registro_izq}, {registro_der}", "comparar !=")
        
        return registro_resultado
    
    def generar_asignacion(self, nodo_asignaciones, ambito):
        """Genera código para asignaciones"""
        nodo_id = buscar_hijo(nodo_asignaciones, 'id')
        nodo_ext = buscar_hijo(nodo_asignaciones, 'ext')
        
        if not nodo_id or not nodo_ext:
            return
            
        nombre_var = nodo_id.valor
        
        # Buscar la expresión a asignar
        nodo_expresion = None
        
        # Caso 1: declaración con tipo
        if nodo_ext.hijos and nodo_ext.hijos[0].tipo == 'tipodato':
            nodo_opcionesasig = buscar_hijo(nodo_ext, 'opcionesasig')
            if nodo_opcionesasig and nodo_opcionesasig.hijos:
                nodo_expresion = buscar_hijo(nodo_opcionesasig, 'expresion')
        
        # Caso 2: asignación directa
        elif nodo_ext.hijos and nodo_ext.hijos[0].tipo == 'extension':
            nodo_extension = nodo_ext.hijos[0]
            nodo_expresion = buscar_hijo(nodo_extension, 'expresion')
        
        if nodo_expresion:
            # Generar código para la expresión
            registro = self.generar_expresion(nodo_expresion, ambito)
            
            if registro:
                # Almacenar en la variable
                offset = self.obtener_offset_variable(nombre_var, ambito)
                if offset is not None:
                    self.agregar_codigo(f"sw {registro}, -{offset}($fp)", f"asignar a {nombre_var}")
    
    def generar_condicional(self, nodo_condicional, ambito):
        """Genera código para estructuras if-else"""
        # Buscar la expresión condicional
        nodo_expresion = buscar_hijo(nodo_condicional, 'expresion')
        
        etiqueta_else = self.nueva_etiqueta("else")
        etiqueta_endif = self.nueva_etiqueta("endif")
        
        if nodo_expresion:
            registro_condicion = self.generar_expresion(nodo_expresion, ambito)
            
            if registro_condicion:
                # Si la condición es falsa (0), saltar al else
                self.agregar_codigo(f"beq {registro_condicion}, $zero, {etiqueta_else}", "saltar si falso")
        
        # Generar código del bloque if
        nodo_instrucciones = buscar_hijo(nodo_condicional, 'masinstrucciones')
        if nodo_instrucciones:
            self.generar_instrucciones(nodo_instrucciones, ambito)
        
        # Saltar al final (evitar ejecutar el else)
        self.agregar_codigo(f"j {etiqueta_endif}", "saltar al final")
        
        # Etiqueta del else
        self.agregar_etiqueta(etiqueta_else)
        
        # Buscar posible bloque else
        nodo_posibilidad = buscar_hijo(nodo_condicional, 'posibilidad')
        if nodo_posibilidad and nodo_posibilidad.hijos:
            primer_hijo = nodo_posibilidad.hijos[0]
            if primer_hijo.tipo == 'sino':
                # Hay bloque else
                nodo_instrucciones_else = buscar_hijo(nodo_posibilidad, 'masinstrucciones')
                if nodo_instrucciones_else:
                    self.generar_instrucciones(nodo_instrucciones_else, ambito)
            elif primer_hijo.tipo == 'entonces':
                # Hay bloque entonces (else-if)
                nodo_instrucciones_entonces = buscar_hijo(nodo_posibilidad, 'masinstrucciones')
                if nodo_instrucciones_entonces:
                    self.generar_instrucciones(nodo_instrucciones_entonces, ambito)
        
        # Etiqueta del final
        self.agregar_etiqueta(etiqueta_endif)
    
    def generar_while(self, nodo_while, ambito):
        """Genera código para bucles while"""
        etiqueta_inicio = self.nueva_etiqueta("while_start")
        etiqueta_fin = self.nueva_etiqueta("while_end")
        
        # Etiqueta del inicio del bucle
        self.agregar_etiqueta(etiqueta_inicio)
        
        # Evaluar condición
        nodo_expresion = buscar_hijo(nodo_while, 'expresion')
        if nodo_expresion:
            registro_condicion = self.generar_expresion(nodo_expresion, ambito)
            
            if registro_condicion:
                # Si la condición es falsa, salir del bucle
                self.agregar_codigo(f"beq {registro_condicion}, $zero, {etiqueta_fin}", "salir si falso")
        
        # Generar código del cuerpo
        nodo_instrucciones = buscar_hijo(nodo_while, 'masinstrucciones')
        if nodo_instrucciones:
            self.generar_instrucciones(nodo_instrucciones, ambito)
        
        # Volver al inicio del bucle
        self.agregar_codigo(f"j {etiqueta_inicio}", "volver al inicio del bucle")
        
        # Etiqueta del final
        self.agregar_etiqueta(etiqueta_fin)
    
    def generar_return(self, nodo_return, ambito):
        """Genera código para return"""
        nodo_expresion = buscar_hijo(nodo_return, 'expresion')
        if nodo_expresion:
            # El valor de retorno va en $v0
            self.generar_expresion(nodo_expresion, ambito, "$v0")
        
        if self.en_funcion and self.en_funcion != 'main':
            # Restaurar frame pointer y retornar
            self.agregar_codigo("move $sp, $fp", "restaurar stack pointer")
            self.agregar_codigo("lw $fp, 0($sp)", "restaurar frame pointer")
            self.agregar_codigo("lw $ra, 4($sp)", "restaurar return address")
            self.agregar_codigo("addiu $sp, $sp, 8", "limpiar stack")
            self.agregar_codigo("jr $ra", "retornar")
        else:
            # Para main, terminar programa
            self.agregar_codigo("li $v0, 10", "system call para exit")
            self.agregar_codigo("syscall", "terminar programa")
    
    def generar_instruccion(self, nodo_instruccion, ambito):
        """Genera código para una instrucción individual"""
        if not nodo_instruccion.hijos:
            return
            
        tipo_instruccion = nodo_instruccion.hijos[0]
        
        if tipo_instruccion.tipo == 'asignaciones':
            self.generar_asignacion(tipo_instruccion, ambito)
        elif tipo_instruccion.tipo == 'condicional':
            self.generar_condicional(tipo_instruccion, ambito)
        elif tipo_instruccion.tipo == 'buclemientras':
            self.generar_while(tipo_instruccion, ambito)
        elif tipo_instruccion.tipo == 'devolver':
            self.generar_return(nodo_instruccion, ambito)
    
    def generar_instrucciones(self, nodo_masinstrucciones, ambito):
        """Genera código para múltiples instrucciones"""
        if not nodo_masinstrucciones or not nodo_masinstrucciones.hijos:
            return
            
        for hijo in nodo_masinstrucciones.hijos:
            if hijo.tipo == 'instruccion':
                self.generar_instruccion(hijo, ambito)
            elif hijo.tipo == 'masinstrucciones':
                self.generar_instrucciones(hijo, ambito)
    
    def generar_funcion(self, nodo_funcion, ambito, nombre_funcion):
        """Genera código para una función con soporte para recursividad"""
        self.en_funcion = nombre_funcion
        self.offset_variables.clear()
        self.offset_actual = 0
        
        # Agregar función a la lista de declaradas
        self.funciones_declaradas.add(nombre_funcion)
        
        # Etiqueta de la función
        self.agregar_etiqueta(nombre_funcion)
        
        if nombre_funcion != 'main':
            # Prólogo de función (convención MIPS)
            self.agregar_codigo("addiu $sp, $sp, -8", "reservar espacio para $fp y $ra")
            self.agregar_codigo("sw $ra, 4($sp)", "guardar return address")
            self.agregar_codigo("sw $fp, 0($sp)", "guardar frame pointer")
            self.agregar_codigo("move $fp, $sp", "establecer nuevo frame pointer")
            
            # Reservar espacio adicional para variables locales
            # (se calculará dinámicamente)
        
        # Generar código para el cuerpo de la función
        nodo_instrucciones = buscar_hijo(nodo_funcion, 'masinstrucciones')
        if nodo_instrucciones:
            # Usar el ámbito de la función
            if ambito.hijos:
                ambito_funcion = ambito.hijos[0]
                
                # Reservar espacio para variables locales
                if self.offset_variables:
                    max_offset = max(self.offset_variables.values())
                    self.agregar_codigo(f"addiu $sp, $sp, -{max_offset}", "reservar espacio para variables locales")
                
                self.generar_instrucciones(nodo_instrucciones, ambito_funcion)
        
        # Epílogo por defecto (si no hay return explícito)
        if nombre_funcion == 'main':
            self.agregar_codigo("li $v0, 10", "system call para exit")
            self.agregar_codigo("syscall", "terminar programa")
        else:
            # Retorno por defecto para funciones
            self.agregar_codigo("li $v0, 0", "valor de retorno por defecto")
            self.agregar_codigo("move $sp, $fp", "restaurar stack pointer")
            self.agregar_codigo("lw $fp, 0($sp)", "restaurar frame pointer")
            self.agregar_codigo("lw $ra, 4($sp)", "restaurar return address")
            self.agregar_codigo("addiu $sp, $sp, 8", "limpiar stack")
            self.agregar_codigo("jr $ra", "retornar")
        
        self.agregar_codigo("", "")
        self.en_funcion = False
    
    def generar_programa(self, nodo_programa, ambito):
        """Genera código para todo el programa"""
        if nodo_programa.tipo != 'programaprincipal':
            return
        
        # Procesar funciones en el programa
        nodo_actual = nodo_programa
        
        while nodo_actual and nodo_actual.tipo == 'programaprincipal':
            # Buscar función definida
            nodo_funcion = buscar_hijo(nodo_actual, 'funcion')
            nodo_opcionprincipal = buscar_hijo(nodo_actual, 'opcionprincipal')
            
            if nodo_funcion and nodo_funcion.hijos:
                # Función regular
                nodo_func = nodo_funcion.hijos[0]  # restofuncn
                nodo_id = buscar_hijo(nodo_func, 'id')
                if nodo_id and nodo_id.valor:
                    nombre_func = nodo_id.valor
                    self.generar_funcion(nodo_func, ambito, nombre_func)
                    
            elif nodo_opcionprincipal and nodo_opcionprincipal.hijos:
                # Función main o función regular
                nodo_func = nodo_opcionprincipal.hijos[0]
                if nodo_func.tipo == 'restomain':
                    self.generar_funcion(nodo_func, ambito, 'main')
                elif nodo_func.tipo == 'restofuncn':
                    nodo_id = buscar_hijo(nodo_func, 'id')
                    if nodo_id and nodo_id.valor:
                        nombre_func = nodo_id.valor
                        self.generar_funcion(nodo_func, ambito, nombre_func)
            
            # Continuar con más funciones
            nodo_masfuncn = buscar_hijo(nodo_actual, 'masfuncn')
            if nodo_masfuncn and nodo_masfuncn.hijos:
                nodo_actual = nodo_masfuncn.hijos[0]
            else:
                break
    
    def generar(self, arbol_sintactico, tabla_simbolos):
        """Función principal que genera todo el código MIPS"""
        self.generar_preambulo()
        self.generar_programa(arbol_sintactico, tabla_simbolos)
        
        return '\n'.join(self.codigo)

def guardar_codigo_assembly_mips(codigo_asm, nombre_archivo):
    """Guarda el código assembly MIPS en un archivo"""
    output_folder = 'salida-assembly-mips'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    nombre_archivo_sin_extension = os.path.splitext(nombre_archivo)[0]
    nombre_archivo_salida = f"{nombre_archivo_sin_extension}.asm"
    ruta_salida = os.path.join(output_folder, nombre_archivo_salida)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(codigo_asm)
    
    return ruta_salida