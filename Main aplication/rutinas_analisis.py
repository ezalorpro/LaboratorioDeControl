import control as ctrl 
import numpy as np
from scipy import real, imag


def system_creator(numerador, denominador, dt=None):
    systema = ctrl.tf(numerador, denominador)
    return systema


def rutina_step_plot(self, systema, T):
    U = np.ones_like(T)
    t, y, _ = ctrl.forced_response(systema, T, U)
    self.main.stepGraphicsView1.canvas.axes.clear()
    self.main.stepGraphicsView1.canvas.axes.plot(t, y)
    self.main.stepGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.stepGraphicsView1.canvas.draw()
    self.main.stepGraphicsView1.toolbar.update()
    return t, y


def rutina_impulse_plot(self, systema):
    t, y = ctrl.impulse_response(systema)
    try:
        T = np.arange(0, 2*np.max(t), 0.1)
    except ValueError:
        T = np.arange(0, 100, 0.1)
    
    U = np.zeros_like(T)
    U[0] = 1
    t, y, _ = ctrl.forced_response(systema, T, U)
    self.main.impulseGraphicsView1.canvas.axes.clear()
    self.main.impulseGraphicsView1.canvas.axes.plot(t, y)
    self.main.impulseGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.impulseGraphicsView1.canvas.draw()
    self.main.impulseGraphicsView1.toolbar.update()
    return t, y, T


def rutina_bode_plot(self, systema):
    w = np.logspace(-3,3,5000)
    mag, phase, omega = ctrl.bode(systema, w)
    
    self.main.BodeGraphicsView1.canvas.axes1.clear()
    self.main.BodeGraphicsView1.canvas.axes1.semilogx(omega, 20 * np.log10(mag))
    self.main.BodeGraphicsView1.canvas.axes1.grid(True,which="both", color="lightgray")
    
    self.main.BodeGraphicsView1.canvas.axes2.clear()
    self.main.BodeGraphicsView1.canvas.axes2.semilogx(omega, phase * 180. / np.pi)
    self.main.BodeGraphicsView1.canvas.axes2.grid(True,which="both", color="lightgray")
    
    self.main.BodeGraphicsView1.canvas.draw()
    self.main.BodeGraphicsView1.toolbar.update()
    return mag, phase, omega


def rutina_nyquist_plot(self, systema):
    w = np.logspace(-3,3,5000)
    real, imag, freq = ctrl.nyquist_plot(systema, w)
    
    self.main.NyquistGraphicsView1.canvas.axes.cla()
    self.main.NyquistGraphicsView1.canvas.axes.plot([-1], [0], 'r+')
    
    self.main.NyquistGraphicsView1.canvas.axes.arrow(real[0], imag[0],
                                                    (real[1]-real[0])/2 ,
                                                    (imag[1]-imag[0])/2,
                                                    width=np.max(real)/70)
    
    self.main.NyquistGraphicsView1.canvas.axes.arrow(real[-1], imag[-1],
                                                     (real[-1]-real[-2])/2 ,
                                                     (imag[-1]-imag[-2])/2,
                                                     width=np.max(real)/70)
    
    mindex = int(len(real)/2)
    
    self.main.NyquistGraphicsView1.canvas.axes.arrow(real[mindex], imag[mindex],
                                                    (real[mindex+1]-real[mindex])/2 ,
                                                    (imag[mindex+1]-imag[mindex])/2,
                                                    width=np.max(real)/70)
    
    self.main.NyquistGraphicsView1.canvas.axes.arrow(real[-mindex], -imag[-mindex],
                                                     (real[-mindex]-real[-mindex+1])/2 ,
                                                     (imag[-mindex+1]-imag[-mindex])/2,
                                                     width=np.max(real)/70)
    
    self.main.NyquistGraphicsView1.canvas.axes.plot(real, imag, 'tab:blue')
    self.main.NyquistGraphicsView1.canvas.axes.plot(real, -imag, 'tab:blue')
    self.main.NyquistGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.NyquistGraphicsView1.canvas.draw()
    self.main.NyquistGraphicsView1.toolbar.update()
    
    return real, imag, freq


def rutina_root_locus_plot(self, systema):
    w = np.logspace(-3,3,5000)
    t, y = ctrl.root_locus(systema, w)
    zeros = ctrl.zero(systema)
    polos = ctrl.pole(systema)
    
    self.main.rlocusGraphicsView1.canvas.axes.cla()
    self.main.rlocusGraphicsView1.canvas.axes.plot(real(t), imag(t), 'b')
    self.main.rlocusGraphicsView1.canvas.axes.plot([0, 0], [np.amin(imag(t)), np.amax(imag(t))], 'g' )
    self.main.rlocusGraphicsView1.canvas.axes.scatter(real(polos), imag(polos), marker='x')
    self.main.rlocusGraphicsView1.canvas.axes.scatter(real(zeros), imag(zeros), marker='o')

    self.main.rlocusGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.rlocusGraphicsView1.canvas.draw()
    self.main.rlocusGraphicsView1.toolbar.update()