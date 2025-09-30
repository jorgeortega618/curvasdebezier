import tkinter as tk
from math import comb

# ---------------- Bézier -----------------
def bezier_curve(points, steps=200):
    """Genera puntos de la curva de Bézier dados puntos de control."""
    n = len(points) - 1
    curve = []
    for j in range(steps+1):
        t = j/steps
        x, y = 0, 0
        for i, (px, py) in enumerate(points):
            b = comb(n, i) * (t**i) * ((1-t)**(n-i))
            x += b * px
            y += b * py
        curve.append((x, y))
    return curve

# ---------------- Interfaz -----------------
class BezierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Curvas de Bézier — Computación Gráfica")
        
        # Frame superior para controles
        control_frame = tk.Frame(root)
        control_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        # Selector de grado de curva
        tk.Label(control_frame, text="Grado de curva:").pack(side="left", padx=5)
        self.degree_var = tk.IntVar(value=4)
        tk.Radiobutton(control_frame, text="Lineal (2 pts)", variable=self.degree_var, value=2).pack(side="left")
        tk.Radiobutton(control_frame, text="Cuadrática (3 pts)", variable=self.degree_var, value=3).pack(side="left")
        tk.Radiobutton(control_frame, text="Cúbica (4 pts)", variable=self.degree_var, value=4).pack(side="left")
        
        # Botones
        tk.Button(control_frame, text="Deshacer último punto", command=self.undo_point).pack(side="left", padx=10)
        tk.Button(control_frame, text="Limpiar todo", command=self.clear_all).pack(side="left")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.points = []   # puntos de control actuales (modo creación)
        self.all_curves = []  # lista de todas las curvas dibujadas (con sus puntos de control)
        self.temp_objects = []  # objetos temporales (puntos y polígono de control actual)
        
        # Variables para arrastre
        self.dragging = False
        self.drag_curve_idx = None
        self.drag_point_idx = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Instrucciones
        self.canvas.create_text(400, 30, text="Haz clic para agregar puntos de control. La curva se creará automáticamente.",
                                fill="gray", font=("Arial", 10), tags="instructions")

    def on_mouse_down(self, event):
        """Maneja el clic del ratón: inicia arrastre o agrega punto"""
        x, y = event.x, event.y
        
        # Verificar si se hizo clic cerca de un punto de control existente
        curve_idx, point_idx = self.find_control_point_at(x, y)
        
        if curve_idx is not None:
            # Iniciar arrastre
            self.dragging = True
            self.drag_curve_idx = curve_idx
            self.drag_point_idx = point_idx
            self.drag_start_x = x
            self.drag_start_y = y
            self.canvas.config(cursor="hand2")
        else:
            # Agregar nuevo punto (modo creación)
            self.add_point(x, y)
    
    def on_mouse_drag(self, event):
        """Arrastra un punto de control y actualiza la curva"""
        if self.dragging:
            x, y = event.x, event.y
            
            # Actualizar posición del punto
            curve_data = self.all_curves[self.drag_curve_idx]
            curve_data["points"][self.drag_point_idx] = (x, y)
            
            # Redibujar solo esta curva
            self.redraw_curve(self.drag_curve_idx)
    
    def on_mouse_up(self, event):
        """Finaliza el arrastre"""
        if self.dragging:
            self.dragging = False
            self.drag_curve_idx = None
            self.drag_point_idx = None
            self.canvas.config(cursor="")
    
    def find_control_point_at(self, x, y, threshold=10):
        """Encuentra si hay un punto de control cerca de (x,y)"""
        for curve_idx, curve_data in enumerate(self.all_curves):
            for point_idx, (px, py) in enumerate(curve_data["points"]):
                distance = ((x - px)**2 + (y - py)**2)**0.5
                if distance <= threshold:
                    return curve_idx, point_idx
        return None, None
    
    def add_point(self, x, y):
        """Agrega un punto de control en modo creación"""
        self.points.append((x, y))
        
        # Redibujar puntos de control actuales con etiquetas
        self.redraw_temp_controls()
        
        # Detectar si hay suficientes puntos para una curva
        n = len(self.points)
        required_points = self.degree_var.get()
        
        if n == required_points:
            self.draw_curve()
            self.points = []  # reinicia para permitir varias curvas
            self.clear_temp_objects()

    def draw_curve(self):
        """Dibuja una nueva curva de Bézier con polígono de control"""
        curve = bezier_curve(self.points)
        
        # Crear estructura de datos para la curva con IDs de objetos
        curve_data = {
            "points": self.points.copy(),
            "curve": curve,
            "canvas_objects": []
        }
        
        self.all_curves.append(curve_data)
        
        # Dibujar la curva (esto asignará los IDs)
        self.redraw_curve(len(self.all_curves) - 1)
    
    def redraw_curve(self, curve_idx):
        """Redibuja una curva específica (usado para actualización en tiempo real)"""
        curve_data = self.all_curves[curve_idx]
        
        # Eliminar objetos anteriores de esta curva
        for obj_id in curve_data.get("canvas_objects", []):
            self.canvas.delete(obj_id)
        curve_data["canvas_objects"] = []
        
        # Recalcular curva de Bézier
        curve = bezier_curve(curve_data["points"])
        curve_data["curve"] = curve
        
        # Dibujar polígono de control (líneas punteadas en rojo)
        points = curve_data["points"]
        for i in range(len(points)-1):
            x0, y0 = points[i]
            x1, y1 = points[i+1]
            obj_id = self.canvas.create_line(x0, y0, x1, y1, fill="red", dash=(4, 4), width=1)
            curve_data["canvas_objects"].append(obj_id)
        
        # Dibujar curva de Bézier (línea azul gruesa)
        for i in range(len(curve)-1):
            x0, y0 = curve[i]
            x1, y1 = curve[i+1]
            obj_id = self.canvas.create_line(x0, y0, x1, y1, fill="blue", width=2, smooth=True)
            curve_data["canvas_objects"].append(obj_id)
        
        # Dibujar puntos de control finales (encima de todo)
        for i, (x, y) in enumerate(points):
            r = 5
            obj_id1 = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", outline="darkred", width=2)
            obj_id2 = self.canvas.create_text(x-15, y-15, text=f"P{i}", fill="red", font=("Arial", 10, "bold"))
            curve_data["canvas_objects"].extend([obj_id1, obj_id2])

    def redraw_temp_controls(self):
        """Redibuja los puntos de control temporales y el polígono mientras se agregan puntos"""
        self.clear_temp_objects()
        
        # Dibujar polígono de control temporal (líneas punteadas grises)
        if len(self.points) > 1:
            for i in range(len(self.points)-1):
                x0, y0 = self.points[i]
                x1, y1 = self.points[i+1]
                obj = self.canvas.create_line(x0, y0, x1, y1, fill="gray", dash=(3, 3), width=1)
                self.temp_objects.append(obj)
        
        # Dibujar puntos temporales
        for i, (x, y) in enumerate(self.points):
            r = 4
            obj1 = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="orange", outline="darkorange", width=2)
            obj2 = self.canvas.create_text(x-12, y-12, text=f"P{i}", fill="orange", font=("Arial", 9, "bold"))
            self.temp_objects.extend([obj1, obj2])
    
    def clear_temp_objects(self):
        """Elimina los objetos temporales del canvas"""
        for obj in self.temp_objects:
            self.canvas.delete(obj)
        self.temp_objects = []
    
    def undo_point(self):
        """Deshace el último punto agregado o elimina la última curva"""
        if self.points:
            # Si hay puntos temporales, eliminar el último
            self.points.pop()
            self.redraw_temp_controls()
        elif self.all_curves:
            # Si no hay puntos temporales, eliminar la última curva
            curve_data = self.all_curves.pop()
            for obj_id in curve_data.get("canvas_objects", []):
                self.canvas.delete(obj_id)
    
    def clear_all(self):
        """Limpia todo el canvas"""
        self.canvas.delete("all")
        self.points = []
        self.all_curves = []
        self.temp_objects = []
        # Redibujar instrucciones
        self.canvas.create_text(400, 30, text="Haz clic para agregar puntos de control. La curva se creará automáticamente.",
                                fill="gray", font=("Arial", 10), tags="instructions")

# ---------------- Main -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BezierApp(root)
    root.mainloop()
