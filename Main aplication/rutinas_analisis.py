import control as ctrl 
import numpy as np 

def system_creator(numerador, denominador, dt=None):
    systema = ctrl.tf(numerador, denominador)
    return systema


def rutina_step_plot(self, systema, T):
    U = np.ones_like(T)
    t, y, _ = ctrl.forced_response(systema, T, U)
    self.main.stepGraphicsView1.canvas.axes.clear()
    self.main.stepGraphicsView1.canvas.axes.plot(t, y)
    self.main.stepGraphicsView1.canvas.axes.grid()
    self.main.stepGraphicsView1.canvas.draw()
    return t, y

def rutina_impulse_plot(self, systema):
    t, y = ctrl.impulse_response(systema)
    T = np.arange(0, 2*np.max(t), 0.1)
    U = np.zeros_like(T)
    U[0] = 1
    t, y, _ = ctrl.forced_response(systema, T, U)
    self.main.impulseGraphicsView1.canvas.axes.clear()
    self.main.impulseGraphicsView1.canvas.axes.plot(t, y)
    self.main.impulseGraphicsView1.canvas.axes.grid()
    self.main.impulseGraphicsView1.canvas.draw()
    return t, y, T

def rutina_bode_plot(self, systema):
    w = np.logspace(-3,3,5000)
    mag, phase, omega = ctrl.bode(systema, w)
    
    self.main.BodeGraphicsView1.canvas.axes1.clear()
    self.main.BodeGraphicsView1.canvas.axes1.semilogx(omega, 20 * np.log10(mag))
    self.main.BodeGraphicsView1.canvas.axes1.grid(True,which="both")
    
    self.main.BodeGraphicsView1.canvas.axes2.clear()
    self.main.BodeGraphicsView1.canvas.axes2.semilogx(omega, phase * 180. / np.pi)
    self.main.BodeGraphicsView1.canvas.axes2.grid(True,which="both")
    
    self.main.BodeGraphicsView1.canvas.draw()
    return mag, phase, omega

def rutina_nyquist_plot(self, systema):
    w = np.logspace(-3,3,5000)
    real, imag, freq = ctrl.nyquist_plot(systema, w)
    
    self.main.NyquistGraphicsView1.canvas.axes.clear()
    self.main.NyquistGraphicsView1.canvas.axes.plot(real, imag, 'tab:blue')
    self.main.NyquistGraphicsView1.canvas.axes.plot(real, -imag, 'tab:blue')
    self.main.NyquistGraphicsView1.canvas.axes.grid()
    self.main.NyquistGraphicsView1.canvas.draw()
    
    return real, imag, freq