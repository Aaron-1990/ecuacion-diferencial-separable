"""
Comparación de Solución Analítica vs Método de Euler
para una Ecuación Diferencial Separable

Problema:
    dy/dt = -0.5 * y
    y(0) = 2
    Intervalo: t ∈ [0, 1]
    Paso: h = 0.2

Solución Analítica:
    y(t) = 2 * e^(-0.5t)

Autor: Aaron
Fecha: 2025-11-18
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# MÓDULO 1: DEFINICIÓN DEL PROBLEMA
# ============================================================================

def ecuacion_diferencial(t, y):
    """
    Define la ecuación diferencial: dy/dt = -0.5 * y
    
    Esta ecuación modela un decaimiento exponencial, aplicable a:
    - Decaimiento radioactivo
    - Enfriamiento de objetos (Ley de Newton)
    - Descarga de capacitores
    - Absorción de medicamentos
    
    Parámetros:
        t (float): Tiempo (variable independiente)
        y (float): Valor de la función en el tiempo t
    
    Retorna:
        float: Valor de la derivada dy/dt
    """
    return -0.5 * y


# ============================================================================
# MÓDULO 2: SOLUCIÓN ANALÍTICA (MÉTODO DE SEPARACIÓN DE VARIABLES)
# ============================================================================

def solucion_analitica(t):
    """
    Solución exacta obtenida mediante separación de variables.
    
    Proceso de resolución:
    
    1. Ecuación diferencial: dy/dt = -0.5y
    
    2. Separación de variables:
       dy/y = -0.5 dt
    
    3. Integración:
       ∫(1/y)dy = ∫(-0.5)dt
       ln|y| = -0.5t + C
    
    4. Despeje de y:
       y = e^(-0.5t + C)
       y = e^C · e^(-0.5t)
       y = A · e^(-0.5t)
    
    5. Condición inicial y(0) = 2:
       2 = A · e^0 → A = 2
    
    6. Solución final:
       y(t) = 2 · e^(-0.5t)
    
    Parámetros:
        t (float o array): Tiempo(s) donde evaluar la solución
    
    Retorna:
        float o array: Valor exacto de y(t)
    """
    return 2 * np.exp(-0.5 * t)


# ============================================================================
# MÓDULO 3: SOLUCIÓN NUMÉRICA (MÉTODO DE EULER)
# ============================================================================

def metodo_euler(f, t0, y0, t_final, h):
    """
    Implementación del Método de Euler para EDOs de primer orden.
    
    Algoritmo:
        y_{n+1} = y_n + h * f(t_n, y_n)
    
    donde:
        - y_n: aproximación en el tiempo t_n
        - h: tamaño de paso
        - f(t, y): función que define dy/dt
    
    Características:
        - Método explícito de orden 1
        - Error local: O(h²)
        - Error global: O(h)
        - Simple pero menos preciso que métodos de orden superior
    
    Parámetros:
        f (function): Función que define dy/dt = f(t, y)
        t0 (float): Tiempo inicial
        y0 (float): Condición inicial y(t0)
        t_final (float): Tiempo final
        h (float): Tamaño de paso
    
    Retorna:
        tuple: (array de tiempos, array de aproximaciones)
    """
    # Calcular número de pasos
    n_pasos = int((t_final - t0) / h)
    
    # Inicializar arrays
    t = np.zeros(n_pasos + 1)
    y = np.zeros(n_pasos + 1)
    
    # Condiciones iniciales
    t[0] = t0
    y[0] = y0
    
    # Iteración del método de Euler
    for i in range(n_pasos):
        t[i + 1] = t[i] + h
        y[i + 1] = y[i] + h * f(t[i], y[i])
    
    return t, y


# ============================================================================
# MÓDULO 4: ANÁLISIS DE ERROR
# ============================================================================

def calcular_error(y_exacta, y_aproximada):
    """
    Calcula diferentes métricas de error entre solución exacta y aproximada.
    
    Parámetros:
        y_exacta (array): Valores exactos
        y_aproximada (array): Valores aproximados
    
    Retorna:
        dict: Diccionario con métricas de error
    """
    error_absoluto = np.abs(y_exacta - y_aproximada)
    error_relativo = error_absoluto / np.abs(y_exacta)
    
    metricas = {
        'error_absoluto': error_absoluto,
        'error_relativo': error_relativo,
        'error_abs_max': np.max(error_absoluto),
        'error_abs_medio': np.mean(error_absoluto),
        'error_rel_max': np.max(error_relativo) * 100,  # En porcentaje
        'error_rel_medio': np.mean(error_relativo) * 100
    }
    
    return metricas


# ============================================================================
# MÓDULO 5: VISUALIZACIÓN
# ============================================================================

def visualizar_comparacion(t_euler, y_euler, t_continuo, y_exacta, metricas):
    """
    Genera visualización comparativa entre solución exacta y aproximada.
    
    Parámetros:
        t_euler (array): Tiempos del método de Euler
        y_euler (array): Valores aproximados
        t_continuo (array): Tiempos para solución continua
        y_exacta (array): Valores exactos
        metricas (dict): Métricas de error calculadas
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # ========================================================================
    # Gráfica 1: Comparación de Soluciones
    # ========================================================================
    axes[0].plot(t_continuo, y_exacta, 'b-', linewidth=2.5, 
                 label='Solución Analítica: y(t) = 2e^(-0.5t)', alpha=0.8)
    axes[0].plot(t_euler, y_euler, 'ro-', linewidth=2, markersize=8,
                 label='Método de Euler (h = 0.2)', alpha=0.8)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].set_xlabel('Tiempo t', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('y(t)', fontsize=12, fontweight='bold')
    axes[0].set_title('Comparación: Solución Analítica vs Método de Euler\n' +
                      'Ecuación: dy/dt = -0.5y, y(0) = 2',
                      fontsize=13, fontweight='bold', pad=15)
    axes[0].legend(loc='upper right', fontsize=11, framealpha=0.9)
    axes[0].set_xlim([0, 1])
    
    # Agregar anotación del error máximo
    idx_max_error = np.argmax(metricas['error_absoluto'])
    axes[0].annotate(f'Error máximo: {metricas["error_abs_max"]:.4f}',
                     xy=(t_euler[idx_max_error], y_euler[idx_max_error]),
                     xytext=(t_euler[idx_max_error] + 0.15, y_euler[idx_max_error] + 0.2),
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                     fontsize=10, color='red', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # ========================================================================
    # Gráfica 2: Análisis de Error
    # ========================================================================
    axes[1].plot(t_euler, metricas['error_absoluto'], 'go-', linewidth=2, 
                 markersize=8, label='Error Absoluto |y_exacta - y_euler|')
    axes[1].plot(t_euler, metricas['error_relativo'], 'mo-', linewidth=2,
                 markersize=8, label='Error Relativo')
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].set_xlabel('Tiempo t', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Error', fontsize=12, fontweight='bold')
    axes[1].set_title(f'Análisis de Error del Método de Euler\n' +
                      f'Error Absoluto Máximo: {metricas["error_abs_max"]:.4f} | ' +
                      f'Error Relativo Máximo: {metricas["error_rel_max"]:.2f}%',
                      fontsize=13, fontweight='bold', pad=15)
    axes[1].legend(loc='upper left', fontsize=11, framealpha=0.9)
    axes[1].set_xlim([0, 1])
    
    plt.tight_layout()
    plt.savefig('comparacion_euler_analitica.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica guardada: 'comparacion_euler_analitica.png'")
    plt.show()


# ============================================================================
# MÓDULO 6: GENERACIÓN DE TABLA COMPARATIVA
# ============================================================================

def generar_tabla_resultados(t_euler, y_euler, y_exacta_euler, metricas):
    """
    Genera tabla comparativa de resultados en formato texto.
    
    Parámetros:
        t_euler (array): Tiempos
        y_euler (array): Valores aproximados
        y_exacta_euler (array): Valores exactos en los mismos tiempos
        metricas (dict): Métricas de error
    """
    print("\n" + "="*90)
    print(f"{'TABLA COMPARATIVA DE RESULTADOS':^90}")
    print("="*90)
    print(f"{'t':>10} | {'y(t) Exacta':>15} | {'y(t) Euler':>15} | {'Error Abs.':>15} | {'Error Rel. (%)':>15}")
    print("-"*90)
    
    for i in range(len(t_euler)):
        print(f"{t_euler[i]:>10.2f} | {y_exacta_euler[i]:>15.6f} | {y_euler[i]:>15.6f} | "
              f"{metricas['error_absoluto'][i]:>15.6f} | {metricas['error_relativo'][i]*100:>15.4f}")
    
    print("="*90)
    print(f"\n{'MÉTRICAS DE ERROR':^90}")
    print("-"*90)
    print(f"  • Error Absoluto Máximo:    {metricas['error_abs_max']:.6f}")
    print(f"  • Error Absoluto Medio:     {metricas['error_abs_medio']:.6f}")
    print(f"  • Error Relativo Máximo:    {metricas['error_rel_max']:.4f}%")
    print(f"  • Error Relativo Medio:     {metricas['error_rel_medio']:.4f}%")
    print("="*90 + "\n")


# ============================================================================
# MÓDULO 7: FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta el análisis completo.
    """
    print("="*90)
    print(f"{'RESOLUCIÓN DE ECUACIÓN DIFERENCIAL SEPARABLE':^90}")
    print(f"{'Comparación: Método Analítico vs Método de Euler':^90}")
    print("="*90)
    
    # ------------------------------------------------------------------------
    # Parámetros del problema
    # ------------------------------------------------------------------------
    t0 = 0.0        # Tiempo inicial
    t_final = 1.0   # Tiempo final
    y0 = 2.0        # Condición inicial
    h = 0.2         # Tamaño de paso
    
    print(f"\n{'DEFINICIÓN DEL PROBLEMA':^90}")
    print("-"*90)
    print(f"  Ecuación diferencial: dy/dt = -0.5y")
    print(f"  Condición inicial:    y(0) = {y0}")
    print(f"  Intervalo de tiempo:  t ∈ [{t0}, {t_final}]")
    print(f"  Tamaño de paso:       h = {h}")
    print(f"  Número de pasos:      {int((t_final - t0) / h)}")
    
    print(f"\n{'SOLUCIÓN ANALÍTICA (Separación de Variables)':^90}")
    print("-"*90)
    print("  Proceso:")
    print("    1. dy/dt = -0.5y")
    print("    2. dy/y = -0.5 dt")
    print("    3. ∫(1/y)dy = ∫(-0.5)dt")
    print("    4. ln|y| = -0.5t + C")
    print("    5. y = A·e^(-0.5t)")
    print("    6. Aplicando y(0) = 2: A = 2")
    print("    7. Solución exacta: y(t) = 2·e^(-0.5t)")
    
    # ------------------------------------------------------------------------
    # Solución Numérica: Método de Euler
    # ------------------------------------------------------------------------
    print(f"\n{'SOLUCIÓN NUMÉRICA (Método de Euler)':^90}")
    print("-"*90)
    print("  Aplicando: y_{n+1} = y_n + h·f(t_n, y_n)")
    print("  Calculando aproximaciones...")
    
    t_euler, y_euler = metodo_euler(ecuacion_diferencial, t0, y0, t_final, h)
    
    # ------------------------------------------------------------------------
    # Solución Analítica en los mismos puntos
    # ------------------------------------------------------------------------
    y_exacta_euler = solucion_analitica(t_euler)
    
    # ------------------------------------------------------------------------
    # Solución Analítica continua (para visualización)
    # ------------------------------------------------------------------------
    t_continuo = np.linspace(t0, t_final, 200)
    y_exacta_continua = solucion_analitica(t_continuo)
    
    # ------------------------------------------------------------------------
    # Cálculo de errores
    # ------------------------------------------------------------------------
    print("  Calculando errores...")
    metricas = calcular_error(y_exacta_euler, y_euler)
    
    # ------------------------------------------------------------------------
    # Mostrar tabla de resultados
    # ------------------------------------------------------------------------
    generar_tabla_resultados(t_euler, y_euler, y_exacta_euler, metricas)
    
    # ------------------------------------------------------------------------
    # Visualización
    # ------------------------------------------------------------------------
    print("Generando visualización comparativa...")
    visualizar_comparacion(t_euler, y_euler, t_continuo, y_exacta_continua, metricas)
    
    # ------------------------------------------------------------------------
    # Análisis de convergencia
    # ------------------------------------------------------------------------
    print(f"{'ANÁLISIS DE CONVERGENCIA':^90}")
    print("-"*90)
    print(f"  El método de Euler tiene:")
    print(f"    • Error local:  O(h²) = O({h**2:.4f})")
    print(f"    • Error global: O(h)  = O({h:.4f})")
    print(f"\n  Para reducir el error a la mitad, necesitarías:")
    print(f"    h = {h/2:.2f} (el doble de pasos)")
    print("="*90)
    
    # ------------------------------------------------------------------------
    # Exportar datos
    # ------------------------------------------------------------------------
    datos = np.column_stack((t_euler, y_euler, y_exacta_euler, 
                             metricas['error_absoluto'], 
                             metricas['error_relativo']))
    np.savetxt('resultados_comparacion.csv', datos,
               delimiter=',',
               header='Tiempo,y_Euler,y_Exacta,Error_Absoluto,Error_Relativo',
               comments='', fmt='%.8f')
    print(f"\n✓ Datos exportados: 'resultados_comparacion.csv'")
    print("="*90 + "\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
