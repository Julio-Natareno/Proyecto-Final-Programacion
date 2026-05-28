class Nodo:
    def __init__(self, valor):
        self.valor = str(valor)
        self.izquierdo = None
        self.derecho = None

class ArbolTorneo:
    def __init__(self, niveles_solicitados=10):
        self.raiz = None
        if niveles_solicitados > 10:
            self.max_niveles = 10
        else:
            self.max_niveles = niveles_solicitados

    def obtener_profundidad(self, nodo):
        if nodo is None:
            return 0
        
        prof_izq = self.obtener_profundidad(nodo.izquierdo)
        prof_der = self.obtener_profundidad(nodo.derecho)
        
        return max(prof_izq, prof_der) + 1

    def insertar_raiz(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return True, "Raiz insertada con exito."
        return False, "El arbol ya tiene una raiz."

    def insertar_hijo(self, nodo_padre, valor, direccion):
        if self.obtener_profundidad(self.raiz) >= self.max_niveles:
            return False, f"Limite de {self.max_niveles} niveles alcanzado."
                
        nuevo_nodo = Nodo(valor)
        
        if direccion == 'I': 
            if nodo_padre.izquierdo is None:
                nodo_padre.izquierdo = nuevo_nodo
                return True, "Insertado a la izquierda."
            else:
                return False, "El nodo padre ya tiene un hijo izquierdo."
                
        elif direccion == 'D': 
            if nodo_padre.derecho is None:
                nodo_padre.derecho = nuevo_nodo
                return True, "Insertado a la derecha."
            else:
                return False, "El nodo padre ya tiene un hijo derecho."
                
        return False, "Direccion no valida."

    # ==========================================
    # MODULO 2: RECORRIDOS DEL ARBOL
    # ==========================================

    def recorrido_preorden(self, nodo, resultado=None):
        if resultado is None:
            resultado = []
        if nodo is not None:
            resultado.append(nodo.valor)
            self.recorrido_preorden(nodo.izquierdo, resultado)
            self.recorrido_preorden(nodo.derecho, resultado)
        return resultado

    def recorrido_inorden(self, nodo, resultado=None):
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.recorrido_inorden(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self.recorrido_inorden(nodo.derecho, resultado)
        return resultado

    def recorrido_postorden(self, nodo, resultado=None):
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.recorrido_postorden(nodo.izquierdo, resultado)
            self.recorrido_postorden(nodo.derecho, resultado)
            resultado.append(nodo.valor)
        return resultado

    # ==========================================
    # MODULO VISUAL: ESTRUCTURA PARA EL CANVAS
    # ==========================================
    def obtener_estructura(self, nodo):
        if nodo is None:
            return None
        return {
            "valor": nodo.valor,
            "izquierdo": self.obtener_estructura(nodo.izquierdo),
            "derecho": self.obtener_estructura(nodo.derecho)
        }

    # ==========================================
    # MODULO 3: ALGORITMO DE RECONSTRUCCION
    # ==========================================
    def reconstruir_arbol(self, preorden, inorden):
        if not preorden or not inorden:
            return None
            
        raiz_valor = preorden[0]
        nuevo_nodo = Nodo(raiz_valor)
        
        try:
            indice_raiz = inorden.index(raiz_valor)
        except ValueError:
            return None 
            
        inorden_izq = inorden[:indice_raiz]
        inorden_der = inorden[indice_raiz + 1:]
        
        preorden_izq = preorden[1:1 + len(inorden_izq)]
        preorden_der = preorden[1 + len(inorden_izq):]
        
        nuevo_nodo.izquierdo = self.reconstruir_arbol(preorden_izq, inorden_izq)
        nuevo_nodo.derecho = self.reconstruir_arbol(preorden_der, inorden_der)
        
        return nuevo_nodo