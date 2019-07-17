import control as ctrl 


def system_creator(numerador, denominador, dt=None):
    systema = ctrl.tf(numerador, denominador)
    return systema


def rutina_step_plot(self, systema):
    t, y = ctrl.step_response(systema)
    self.main.stepGraphicsView1.canvas.axes.plot(t, y)
    self.main.stepGraphicsView1.canvas.draw()
    return t, y