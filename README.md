# Curvas de Bézier - Computación Gráfica

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Aplicación interactiva para crear y editar curvas de Bézier de diferentes grados. Permite al usuario dibujar formas arbitrarias mediante puntos de control que pueden ser arrastrados en tiempo real.

## 📋 Descripción

Este proyecto implementa un editor gráfico de curvas de Bézier que permite:
- Crear curvas de Bézier de grado 1 (lineal), 2 (cuadrática) y 3 (cúbica)
- Visualizar el polígono de control con líneas punteadas
- Arrastrar puntos de control para modificar las curvas en tiempo real
- Dibujar figuras complejas mediante múltiples curvas secuenciales

## ✨ Características

### 🎨 Creación de Curvas
- **Selección de grado**: Elige entre curvas lineales (2 puntos), cuadráticas (3 puntos) o cúbicas (4 puntos)
- **Creación interactiva**: Haz clic en el canvas para agregar puntos de control
- **Generación automática**: La curva se crea automáticamente al completar el número de puntos requerido
- **Múltiples curvas**: Dibuja tantas curvas como necesites para formar figuras complejas

### 🖱️ Edición en Tiempo Real
- **Arrastre de puntos**: Haz clic y arrastra cualquier punto de control existente
- **Actualización dinámica**: Las curvas se recalculan y redibujan instantáneamente
- **Detección inteligente**: El programa distingue automáticamente entre agregar puntos y arrastrarlos

### 👁️ Visualización
- **Puntos de control**: Círculos rojos con etiquetas (P0, P1, P2, P3...)
- **Polígono de control**: Líneas punteadas rojas conectando los puntos de control
- **Curva de Bézier**: Línea azul suave que representa la curva matemática
- **Feedback visual**: Puntos temporales en naranja mientras se construye una curva

### 🔧 Herramientas
- **Deshacer**: Elimina el último punto agregado o la última curva completa
- **Limpiar todo**: Reinicia el canvas para comenzar de nuevo

## 🎓 Fundamento Matemático

El proyecto utiliza la fórmula de Bernstein para calcular las curvas de Bézier:

```
B(t) = Σ (i=0 hasta n) [C(n,i) × t^i × (1-t)^(n-i) × P_i]
```

Donde:
- **n**: Grado de la curva (número de puntos - 1)
- **t**: Parámetro de interpolación [0, 1]
- **C(n,i)**: Coeficiente binomial
- **P_i**: Puntos de control

### Grados Soportados

| Grado | Puntos | Tipo | Descripción |
|-------|--------|------|-------------|
| 1 | 2 | Lineal | Línea recta entre dos puntos |
| 2 | 3 | Cuadrática | Curva suave con un punto de control intermedio |
| 3 | 4 | Cúbica | Curva con dos puntos de control intermedios (más flexible) |

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.7 o superior
- Tkinter (incluido por defecto en la mayoría de las instalaciones de Python)

### Verificar Tkinter

```bash
python -m tkinter
```

Si se abre una ventana pequeña, Tkinter está instalado correctamente.

### Ejecutar el Programa

```bash
python bezier_tk.py
```

## 📖 Guía de Uso

### 1. Crear una Curva

1. **Selecciona el grado** deseado usando los radio buttons:
   - Lineal (2 pts)
   - Cuadrática (3 pts)
   - Cúbica (4 pts)

2. **Haz clic** en el canvas para agregar puntos de control
   - Los puntos temporales aparecen en **naranja**
   - Las líneas guía son **grises punteadas**

3. **La curva se crea automáticamente** cuando agregas el último punto requerido
   - Los puntos finales se vuelven **rojos**
   - El polígono de control aparece en **rojo punteado**
   - La curva se dibuja en **azul**

### 2. Editar una Curva

1. **Coloca el cursor** sobre un punto de control existente (círculo rojo)
2. **Haz clic y arrastra** el punto a una nueva posición
3. **La curva se actualiza** en tiempo real mientras arrastras
4. **Suelta** el botón del mouse para finalizar

### 3. Crear Figuras Complejas

- Después de completar una curva, **continúa agregando puntos** para crear la siguiente
- Puedes combinar curvas de diferentes grados
- Ejemplo: Dibuja un carro, una letra, una vasija, etc.

### 4. Herramientas

- **Deshacer último punto**: Elimina el último punto temporal o la última curva completa
- **Limpiar todo**: Borra todas las curvas y reinicia el canvas

## 🎯 Requerimientos Cumplidos

Este proyecto cumple con los siguientes requerimientos académicos:

### ✅ Requerimiento 1
> *"Construir un programa que permita al usuario, dando clic con el ratón en la pantalla, crear puntos de control, una vez ingresado los puntos, se deberá crear la curva de Bézier determinada por los puntos."*

**Implementado**: Sistema de clics para agregar puntos y generación automática de curvas.

### ✅ Requerimiento 2
> *"El usuario podrá determinar formas arbitrarias con el ratón de tal manera que se puedan crear figuras complejas."*

**Implementado**: Soporte para múltiples curvas secuenciales que permanecen en el canvas.

### ✅ Requerimiento 3
> *"El dibujo arbitrario se podrá hacer con curvas de Bézier de grado 2, 3 y 4. De tal manera que cada (2, 3 y 4) puntos se cree una curva de Bézier."*

**Implementado**: Selector de grado con soporte para curvas lineales, cuadráticas y cúbicas.

### ✅ Bonus: Edición Interactiva
> *"El usuario podrá arrastrar con el ratón cualquiera de los puntos de control y el programa debe permitir que la curva siga el punto de control escogido."*

**Implementado**: Sistema de arrastre con actualización en tiempo real de las curvas.

## 🏗️ Estructura del Código

```
bezier_tk.py
├── bezier_curve(points, steps=200)
│   └── Calcula los puntos de la curva de Bézier usando la fórmula de Bernstein
│
└── BezierApp (clase principal)
    ├── __init__(): Inicializa la interfaz y variables
    ├── on_mouse_down(): Maneja clics (arrastre o agregar punto)
    ├── on_mouse_drag(): Actualiza posición durante el arrastre
    ├── on_mouse_up(): Finaliza el arrastre
    ├── find_control_point_at(): Detecta puntos cercanos al cursor
    ├── add_point(): Agrega un nuevo punto de control
    ├── draw_curve(): Crea una nueva curva completa
    ├── redraw_curve(): Redibuja una curva específica (para arrastre)
    ├── redraw_temp_controls(): Dibuja puntos temporales
    ├── clear_temp_objects(): Limpia objetos temporales
    ├── undo_point(): Deshace último punto o curva
    └── clear_all(): Limpia todo el canvas
```

## 🎨 Convenciones Visuales

| Elemento | Color | Estilo | Uso |
|----------|-------|--------|-----|
| Puntos temporales | Naranja | Círculo sólido | Mientras se crea una curva |
| Puntos finales | Rojo | Círculo con borde | Puntos de control de curvas completadas |
| Polígono temporal | Gris | Línea punteada | Conexión entre puntos temporales |
| Polígono de control | Rojo | Línea punteada | Conexión entre puntos de control |
| Curva de Bézier | Azul | Línea suave gruesa | La curva matemática resultante |
| Etiquetas | Naranja/Rojo | Texto | Identificadores de puntos (P0, P1...) |

## 🔬 Algoritmo

### Fórmula de Bernstein

El algoritmo implementa la definición matemática de las curvas de Bézier:

```python
def bezier_curve(points, steps=200):
    n = len(points) - 1  # Grado de la curva
    curve = []
    for j in range(steps + 1):
        t = j / steps  # Parámetro de interpolación
        x, y = 0, 0
        for i, (px, py) in enumerate(points):
            # Polinomio de Bernstein
            b = comb(n, i) * (t**i) * ((1-t)**(n-i))
            x += b * px
            y += b * py
        curve.append((x, y))
    return curve
```

### Complejidad

- **Tiempo**: O(n × m) donde n = número de puntos de control, m = steps (resolución)
- **Espacio**: O(m) para almacenar los puntos de la curva

## 🛠️ Posibles Extensiones

- [ ] Exportar imagen a PNG/SVG
- [ ] Guardar/cargar proyectos (JSON)
- [ ] Animación del parámetro t
- [ ] Subdivisión de De Casteljau
- [ ] Curvas B-Spline
- [ ] Superficies de Bézier (3D)
- [ ] Continuidad C0, C1, C2 entre curvas
- [ ] Colores personalizables

## 📚 Referencias

- **Bézier, P.** (1972). *Numerical Control: Mathematics and Applications*
- **Farin, G.** (2002). *Curves and Surfaces for CAGD: A Practical Guide*
- **Rogers, D.F.** (2001). *An Introduction to NURBS*

## 👨‍💻 Autores

- Juan Acosta
- Laura Arteta
- Jorge Ortega



## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Disfruta creando curvas de Bézier! 🎨✨**
