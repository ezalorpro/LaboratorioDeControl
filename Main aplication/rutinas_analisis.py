import control as ctrl 
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt


def system_creator(self, numerador, denominador):
    system = ctrl.tf(numerador, denominador)
    
    t, y = ctrl.impulse_response(system)
    
    if self.main.tfdiscretocheckBox1.isChecked():
            system = ctrl.sample_system(system, self.dt)
    
    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, 2*np.max(t), self.dt)
        else:
            T = np.arange(0, 2*np.max(t), 0.01)      
    except ValueError:
        T = np.arange(0, 100, 0.1)
        
    return system, T


def rutina_step_plot(self, system, T):
    U = np.ones_like(T)
    t, y, _ = ctrl.forced_response(system, T, U)
            
    self.main.stepGraphicsView1.canvas.axes.clear()
    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.stepGraphicsView1.canvas.axes.step(t, y)
    else:
        self.main.stepGraphicsView1.canvas.axes.plot(t, y)
        
    self.main.stepGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.stepGraphicsView1.canvas.draw()
    self.main.stepGraphicsView1.toolbar.update()
    return t, y


def rutina_impulse_plot(self, system, T):
    
    U = np.zeros_like(T)
    U[0] = 1
    t, y, _ = ctrl.forced_response(system, T, U)
            
    self.main.impulseGraphicsView1.canvas.axes.clear()
    
    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.impulseGraphicsView1.canvas.axes.step(t, y)
    else:
        self.main.impulseGraphicsView1.canvas.axes.plot(t, y)
        
    self.main.impulseGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.impulseGraphicsView1.canvas.draw()
    self.main.impulseGraphicsView1.toolbar.update()
    return t, y


def rutina_bode_plot(self, system):
    
    if ctrl.isdtime(system, strict=True):
        w = np.logspace(-np.pi, 2*np.pi, 5000)
        mag, phase, omega = ctrl.bode(system, w)
    else:
        w = np.logspace(-np.pi, 2*np.pi, 5000)
        mag, phase, omega = ctrl.bode(system, w)
    
    self.main.BodeGraphicsView1.canvas.axes1.clear()
    self.main.BodeGraphicsView1.canvas.axes1.semilogx(omega, 20 * np.log10(mag))
    self.main.BodeGraphicsView1.canvas.axes1.grid(True,which="both", color="lightgray")
    
    self.main.BodeGraphicsView1.canvas.axes2.clear()
    self.main.BodeGraphicsView1.canvas.axes2.semilogx(omega, phase * 180. / np.pi)
    self.main.BodeGraphicsView1.canvas.axes2.grid(True,which="both", color="lightgray")
    
    self.main.BodeGraphicsView1.canvas.draw()
    self.main.BodeGraphicsView1.toolbar.update()
    return mag, phase, omega


def rutina_nyquist_plot(self, system):
        
    if ctrl.isdtime(system, strict=True):
        w = np.linspace(-np.pi, 2*np.pi, 5000)
        real, imag, freq = ctrl.nyquist_plot(system, w)
    else:
        w = np.linspace(-np.pi, 2*np.pi, 5000)
        print('hola')
        real, imag, freq = ctrl.nyquist_plot(system, w)
    
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


def rutina_root_locus_plot(self, system):
    t, y = ctrl.root_locus(system)
    
    zeros = ctrl.zero(system)
    polos = ctrl.pole(system)
    
    self.main.rlocusGraphicsView1.canvas.axes.cla()
    self.main.rlocusGraphicsView1.canvas.axes.plot(real(t), imag(t), 'b')
    self.main.rlocusGraphicsView1.canvas.axes.plot([0, 0], [np.amin(imag(t)), np.amax(imag(t))], 'g' )
    self.main.rlocusGraphicsView1.canvas.axes.scatter(real(polos), imag(polos), marker='x')
    self.main.rlocusGraphicsView1.canvas.axes.scatter(real(zeros), imag(zeros), marker='o')

    self.main.rlocusGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.rlocusGraphicsView1.canvas.draw()
    self.main.rlocusGraphicsView1.toolbar.update()
