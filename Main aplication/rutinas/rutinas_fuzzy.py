import numpy as np
from skfuzzymdf import control as fuzz
from skfuzzymdf.membership import generatemf
from skfuzzymdf.control.visualization import FuzzyVariableVisualizer
from skfuzzymdf.control.controlsystem import CrispValueCalculator
from skfuzzymdf.fuzzymath.fuzzy_ops import interp_membership
from collections import OrderedDict
import pickle
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
import pyqtgraph as pg
import copy


class FuzzyController():
    def __init__(self, inputlist, outputlist, rulelist=[]):
        self.fuzz_inputs = self.crear_input(inputlist)
        self.fuzz_outputs = self.crear_output(outputlist)
        self.flagpyqt = 1
        
        self.colors = [
            '#1f77b4',
            '#ff7f0e',
            '#2ca02c',
            '#d62728',
            '#9467bd',
            '#8c564b',
            '#e377c2',
            '#7f7f7f',
            '#bcbd22',
            '#17becf'
        ]
        self.inlabelsplot = []
        self.inareas = []
        self.invalues = []
        
        self.outlabelsplot = []
        self.outareas = []
        self.outvalues = []
        
        self.rulelist = []
        
        self.crear_etiquetas_input(inputlist)
        self.crear_etiquetas_output(outputlist)
        
        if len(rulelist) > 0:
            self.crear_reglas(rulelist)
            self.crear_controlador()     
        
    def crear_input(self, inputlist):
        vector = []
        for i, ins in enumerate(inputlist):
            temp_in = fuzz.Antecedent(np.linspace(*ins['rango'], 500), ins['nombre'])
            vector.append(temp_in)
        return vector
    
    def crear_output(self, outputlist):
        vector = []
        for i, ins in enumerate(outputlist):
            temp_in = fuzz.Consequent(np.linspace(*ins['rango'], 500), ins['nombre'], ins['metodo'])
            vector.append(temp_in)
        return vector
    
    def crear_etiquetas_input(self, inputlist):
        
        for n, i in enumerate(inputlist):
            for eti in i['etiquetas']:
                self.fuzz_inputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[n].universe, *eti['definicion'])

    def crear_etiquetas_output(self, outputlist):
        for n, i in enumerate(outputlist):
            for eti in i['etiquetas']:
                self.fuzz_outputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[n].universe, *eti['definicion'])

    def graficar_mf_in(self, window, i):
        window.main.inputgraphicsView.canvas.axes.clear()
        FuzzyVariableVisualizer(self.fuzz_inputs[i], 
                                window.main.inputgraphicsView, 
                                window.main.inputgraphicsView.canvas.axes).view_gui()
        window.main.inputgraphicsView.canvas.axes.grid(color="lightgray")
        window.main.inputgraphicsView.canvas.draw()
        window.main.inputgraphicsView.toolbar.update()
    
    def graficar_mf_out(self, window, o):
        window.main.outputgraphicsView.canvas.axes.clear()
        FuzzyVariableVisualizer(self.fuzz_outputs[o], 
                                window.main.outputgraphicsView, 
                                window.main.outputgraphicsView.canvas.axes).view_gui()
        window.main.outputgraphicsView.canvas.axes.grid(color="lightgray")
        window.main.outputgraphicsView.canvas.draw()
        window.main.outputgraphicsView.toolbar.update()
        
    def cambiar_nombre_input(self, window, i, nombre):
        self.fuzz_inputs[i].label = nombre
        self.graficar_mf_in(window, i)
    
    def cambiar_nombre_output(self, window, o, nombre):
        self.fuzz_outputs[o].label = nombre
        self.graficar_mf_out(window, o)
        
    def cambio_etiquetas_input(self, window, inputlist, i):
        self.fuzz_inputs[i].terms = OrderedDict()
        self.crear_etiquetas_input(inputlist)
        self.graficar_mf_in(window, i)
    
    def cambio_etiquetas_output(self, window, outputlist, o):
        self.fuzz_outputs[o].terms = OrderedDict()
        self.crear_etiquetas_output(outputlist)
        self.graficar_mf_out(window, o)
    
    def update_rango_input(self, window, inputlist, i):
        self.fuzz_inputs[i].universe = np.asarray(np.linspace(*inputlist[i]['rango'], 500))
        self.graficar_mf_in(window, i)
    
    def update_rango_output(self, window, outputlist, o):
        self.fuzz_outputs[o].universe = np.asarray(np.linspace(*outputlist[o]['rango'], 500))
        self.graficar_mf_out(window, o)
    
    def cambiar_metodo(self, window, o, metodo):
        self.fuzz_inputs[o].defuzzify_method = metodo
             
    def cambio_etinombre_input( self, window, inputlist, i, n, old_name):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i].terms.pop(old_name)    
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)
    
    def cambio_etinombre_output( self, window, outputlist, o, n, old_name):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o].terms.pop(old_name)    
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[o].universe, *eti['definicion'])
        self.graficar_mf_out(window, o)
        
    def update_definicion_input(self, window, inputlist, i, n):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)
        
    def update_definicion_output(self, window, outputlist, o, n):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[o].universe, *eti['definicion'])
        self.graficar_mf_out(window, o)

    def crear_reglas(self, rulelistC):
        for sets in rulelistC:
            Etiquetasin, Etiquetasout, logica = copy.deepcopy(sets)
            
            self.rulelist.append(fuzz.Rule())
         
            inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
            
            if not negacion_ini:
                self.rulelist[-1].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
            else:
                self.rulelist[-1].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
                
            outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
            
            self.rulelist[-1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
            
            for i in Etiquetasin[1:len(Etiquetasin)]:
                if logica:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
                else:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
            
            for o in Etiquetasout[1:len(Etiquetasout)]:
                self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])
        
        return self.rulelist
    
    def agregar_regla(self, window, ni, no, Etiquetasin, Etiquetasout):
        
        self.rulelist.append(fuzz.Rule())
         
        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
        
        if not negacion_ini:
            self.rulelist[-1].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
        else:
            self.rulelist[-1].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
            
        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
        
        self.rulelist[-1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
        
        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
        
        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])

        return self.rulelist[-1]
    
    def eliminar_regla(self, index_rule):
        del self.rulelist[index_rule]
    
    def cambiar_regla(self, window, ni, no, Etiquetasin, Etiquetasout, index_rule):
        del self.rulelist[index_rule]
        self.rulelist.insert(index_rule, fuzz.Rule())
        
        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
        
        if not negacion_ini:
            self.rulelist[index_rule].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
        else:
            self.rulelist[index_rule].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
            
        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
        
        self.rulelist[index_rule].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
        
        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
        
        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[index_rule].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])

        return self.rulelist[index_rule]
    
    def crear_controlador(self):
        temp = fuzz.ControlSystem(self.rulelist)
        self.Controlador = fuzz.ControlSystemSimulation(temp, flush_after_run=20000)
        
    def prueba_de_controlador(self, window, values, ni, no, pyqtgraph=False):
        for i in range(ni):
            self.Controlador.input[self.fuzz_inputs[i].label] = values[i]
            
        self.Controlador.compute()
        if not pyqtgraph:
            self.graficar_prueba(window, ni, no)
        else:
            if self.flagpyqt:
                self.crear_plots_in(window, values, ni, no)
                self.crear_plots_out(window, values, ni, no)
                self.flagpyqt = 0
            self.graficar_prueba_pyqtgraph(window, ni, no)
    
    def graficar_prueba(self, window, ni, no):
        for i, grafica in enumerate(window.ingraphs[:ni]):
            grafica.canvas.axes.clear()
            FuzzyVariableVisualizer(self.fuzz_inputs[i], 
                                    grafica, 
                                    grafica.canvas.axes).view_gui(self.Controlador, legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()
            
        for o, grafica in enumerate(window.outgraphs[:no]):
            grafica.canvas.axes.clear()
            value = FuzzyVariableVisualizer(self.fuzz_outputs[o], 
                                    grafica, 
                                    grafica.canvas.axes).view_gui(self.Controlador, legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()
            
            window.outtestlabels[o].setText(window.OutputList[o]['nombre'] + f': {np.around(value, 3)}')
    
    def crear_plots_in(self, window, values, ni, no):
        for i in range(ni):
            window.ingraphs[i].plotwidget.clear()
            window.ingraphs[i].plotwidget.setXRange(*window.InputList[i]['rango'], 0.02)
            
            entradas = []
            areas = []
            
            crispy = CrispValueCalculator(self.fuzz_inputs[i], self.Controlador)
            ups_universe, output_mf, cut_mfs = crispy.find_memberships()
            zeros = np.zeros_like(ups_universe, dtype=np.float64)
            
            color = 0
            for key, term in self.fuzz_inputs[i].terms.items():
                entradas.append(window.ingraphs[i].plotwidget.plot(self.fuzz_inputs[i].universe, term.mf, pen={'width': 2, 'color':pg.mkColor(self.colors[color])}))
                
                under_plot = window.ingraphs[i].plotwidget.plot(ups_universe, zeros, pen={'width': 0.1, 'color':pg.mkColor(self.colors[color] + '6A')})
                
                over_plot = window.ingraphs[i].plotwidget.plot(ups_universe, cut_mfs[key], pen={'width': 0.1, 'color':pg.mkColor(self.colors[color] + '6A')})
                
                fillItem = pg.FillBetweenItem(under_plot, over_plot, brush=pg.mkColor(self.colors[color] + '6A'))
                
                window.ingraphs[i].plotwidget.addItem(fillItem)
                areas.append(copy.copy([under_plot, over_plot]))
                color += 1
            
            if len(cut_mfs) > 0 and not all(output_mf == 0):
                crisp_value = self.fuzz_inputs[i].input[self.Controlador]

                # Draw the crisp value at the actual cut height
                if crisp_value is not None:
                    y = 0.
                    for key, term in self.fuzz_inputs[i].terms.items():
                        if key in cut_mfs:
                            y = max(y, interp_membership(self.fuzz_inputs[i].universe,
                                                        term.mf, crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    crispPlot = window.ingraphs[i].plotwidget.plot([crisp_value] * 2, np.asarray([0, y]), pen={'width': 6, 'color':'k'})
                    
                else:
                    crisp_value= 0
            else:
                crisp_value = 0
            
            self.invalues.append(crispPlot)        
            self.inlabelsplot.append(copy.copy(entradas))
            self.inareas.append(copy.copy(areas))
    
    def crear_plots_out(self, window, values, ni, no):
        for i in range(no):
            window.outgraphs[i].plotwidget.clear()
            window.outgraphs[i].plotwidget.setXRange(*window.OutputList[i]['rango'], 0.02)
            
            salidas = []
            areas = []
            
            crispy = CrispValueCalculator(self.fuzz_outputs[i], self.Controlador)
            ups_universe, output_mf, cut_mfs = crispy.find_memberships()
            zeros = np.zeros_like(ups_universe, dtype=np.float64)
            
            color = 0
            for key, term in self.fuzz_outputs[i].terms.items():
                salidas.append(window.outgraphs[i].plotwidget.plot(self.fuzz_outputs[i].universe, term.mf, pen={'width': 2, 'color':pg.mkColor(self.colors[color])}))
                
                under_plot = window.outgraphs[i].plotwidget.plot(ups_universe, zeros, pen={'width': 0.1, 'color':pg.mkColor(self.colors[color] + '6A')})
                
                over_plot = window.outgraphs[i].plotwidget.plot(ups_universe, cut_mfs[key], pen={'width': 0.1, 'color':pg.mkColor(self.colors[color] + '6A')})
                
                fillItem = pg.FillBetweenItem(under_plot, over_plot, brush=pg.mkColor(self.colors[color] + '6A'))
                
                window.outgraphs[i].plotwidget.addItem(fillItem)
                areas.append(copy.copy([under_plot, over_plot]))
                color += 1
            
            if len(cut_mfs) > 0 and not all(output_mf == 0):
                crisp_value = self.fuzz_outputs[i].output[self.Controlador]

                # Draw the crisp value at the actual cut height
                if crisp_value is not None:
                    y = 0.
                    for key, term in self.fuzz_outputs[i].terms.items():
                        if key in cut_mfs:
                            y = max(y, interp_membership(self.fuzz_outputs[i].universe,
                                                        term.mf, crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    crispPlot = window.outgraphs[i].plotwidget.plot([crisp_value] * 2, np.asarray([0, y]), pen={'width': 6, 'color':'k'})
                    
                else:
                    crisp_value= 0
            else:
                crisp_value = 0
            
            self.outvalues.append(crispPlot)         
            self.outlabelsplot.append(copy.copy(salidas))
            self.outareas.append(copy.copy(areas))
    
    def graficar_prueba_pyqtgraph(self, window, ni, no):
        for i in range(ni):
            crispy = CrispValueCalculator(self.fuzz_inputs[i], self.Controlador)
            ups_universe, output_mf, cut_mfs = crispy.find_memberships()
            zeros = np.zeros_like(ups_universe, dtype=np.float64)
            
            for etiq, label in enumerate(window.InputList[i]['etiquetas']):
                self.inlabelsplot[i][etiq].setData(self.fuzz_inputs[i].universe, self.fuzz_inputs[i].terms[label['nombre']].mf)
                under_plot, over_plot = self.inareas[i][etiq]
                under_plot.setData(ups_universe, zeros)
                over_plot.setData(ups_universe, cut_mfs[label['nombre']])
            
            if len(cut_mfs) > 0 and not all(output_mf == 0):
                crisp_value = self.fuzz_inputs[i].input[self.Controlador]
                if crisp_value is not None:
                    y = 0.
                    for key, term in self.fuzz_inputs[i].terms.items():
                        if key in cut_mfs:
                            y = max(y, interp_membership(self.fuzz_inputs[i].universe,
                                                        term.mf, crisp_value))
                    if y < 0.1:
                        y = 1.

                    self.invalues[i].setData([crisp_value] * 2, np.asarray([0, y]))
                else:
                    crisp_value= 0
            else:
                crisp_value = 0
        
        for i in range(no):
            crispy = CrispValueCalculator(self.fuzz_outputs[i], self.Controlador)
            ups_universe, output_mf, cut_mfs = crispy.find_memberships()
            zeros = np.zeros_like(ups_universe, dtype=np.float64)
            
            for etiq, label in enumerate(window.OutputList[i]['etiquetas']):
                self.outlabelsplot[i][etiq].setData(self.fuzz_outputs[i].universe, self.fuzz_outputs[i].terms[label['nombre']].mf)
                under_plot, over_plot = self.outareas[i][etiq]
                under_plot.setData(ups_universe, zeros)
                over_plot.setData(ups_universe, cut_mfs[label['nombre']])
            
            if len(cut_mfs) > 0 and not all(output_mf == 0):
                crisp_value = self.fuzz_outputs[i].output[self.Controlador]

                # Draw the crisp value at the actual cut height
                if crisp_value is not None:
                    y = 0.
                    for key, term in self.fuzz_outputs[i].terms.items():
                        if key in cut_mfs:
                            y = max(y, interp_membership(self.fuzz_outputs[i].universe,
                                                        term.mf, crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    self.outvalues[i].setData([crisp_value] * 2, np.asarray([0, y]))
                    
                else:
                    crisp_value= 0
            else:
                crisp_value = 0

            window.outtestlabels[i].setText(window.OutputList[i]['nombre'] + f': {np.around(crisp_value, 3)}')
            
    def graficar_respuesta_2d(self, window, inrange, no):
        entrada = np.linspace(*inrange, 500)
        
        entradas = []
        salidas = [[] for i in range(no)]
        
        for value in entrada :
            self.Controlador.input[self.fuzz_inputs[0].label] = value
            try:
                self.Controlador.compute()
                entradas.append(value)
                for i in range(no):
                    salidas[i].append(self.Controlador.output[self.fuzz_outputs[i].label])
            except:
                pass
        
        for i in range(no):
            window.respuesta2ds[i].canvas.axes.clear()
            window.respuesta2ds[i].canvas.axes.plot(entradas, salidas[i])
            window.respuesta2ds[i].canvas.axes.grid(color="lightgray")
            window.respuesta2ds[i].canvas.axes.set_xlabel(self.fuzz_inputs[0].label)
            window.respuesta2ds[i].canvas.axes.set_ylabel(self.fuzz_outputs[i].label)
            window.respuesta2ds[i].canvas.draw()
            window.respuesta2ds[i].toolbar.update()
    
    def graficar_respuesta_3d(self, window, inrange1, inrange2, no):
        n_puntos = 20
        entrada1 = np.linspace(*inrange1, n_puntos)
        entrada2 = np.linspace(*inrange2, n_puntos)
        entrada1, entrada2 = np.meshgrid(entrada1, entrada2)
        
        entrada11 = [np.zeros_like(entrada1) for i in range(no)]
        entrada22 = [np.zeros_like(entrada2) for i in range(no)]
        
        salidas = [np.zeros_like(entrada1) for i in range(no)]
		
        for i in range(n_puntos) :
            for j in range(n_puntos):
                self.Controlador.input[self.fuzz_inputs[0].label] = entrada1[i, j]
                self.Controlador.input[self.fuzz_inputs[1].label] = entrada2[i, j]
                try:
                    self.Controlador.compute()
                    for o in range(no):
                        entrada11[o][i, j] =  entrada1[i, j]
                        entrada22[o][i, j] = entrada2[i, j]
                        salidas[o][i, j] = self.Controlador.output[self.fuzz_outputs[o].label]
                except:
                    pass
                     
        for o in range(no):
            # Cross-in-tray
            # x_samp = np.linspace(-10, 10, 20)
            # y_samp = np.linspace(-10, 10, 20)
            # x, y = np.meshgrid(x_samp, y_samp)
            # Total_puntos = len(x)*len(y)

            # a = -0.0001

            # z = a*(np.abs(np.sin(x)*np.sin(y)*np.exp(np.abs(100-np.sqrt(x**2 + y**2)/np.pi))) + 1)**0.1
            
            
            # print(z)
            # print(salidas[o])
            # salidas[o] = z
            # entrada11[o] = x
            # entrada22[o] = y
            x = copy.deepcopy(entrada11[o])
            y = copy.deepcopy(entrada22[o])
            z = copy.deepcopy(salidas[o])
            
            # with open('probando.pkl', 'wb', ) as f:
            #     pickle.dump([x, y, z], f)
                
            window.respuesta3ds[o].vtk_widget.clear()
            window.respuesta3ds[o].vtk_widget.remove_bounds_axes()
            
            window.respuesta3ds[o].vtk_widget.set_scale(xscale=(np.max(z)/np.max(x)),
                                                        yscale=(np.max(z)/np.max(y)))
            
            grid = pv.StructuredGrid(x, y, z)
            
            window.respuesta3ds[o].vtk_widget.add_mesh(grid, 
                                                       scalars=z.ravel(), 
                                                       cmap='viridis', 
                                                       style='surface',
                                                       interpolate_before_map=True,
                                                       lighting=False)
            
            window.respuesta3ds[o].vtk_widget.show_bounds(grid='back',
                                                          location='outer',
                                                          ticks='both',
                                                          bounds=[np.min(x), np.max(x),
                                                                  np.min(y), np.max(y),
                                                                  np.min(z), np.max(z)])
            
            window.respuesta3ds[o].vtk_widget.add_scalar_bar()
            window.respuesta3ds[o].vtk_widget.show_axes()
            window.respuesta3ds[o].vtk_widget.update_bounds_axes()
            window.respuesta3ds[o].vtk_widget.update()
            
            
            # window.respuesta3ds[o].canvas.axes.clear()
            
            # if window.respuesta3ds[o].colorbar != 0:
            #     window.respuesta3ds[o].colorbar.remove()
                
            # surface = window.respuesta3ds[o].canvas.axes.plot_surface(entrada11[o], entrada22[o], salidas[o], 
            #                                                 rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
            
            # window.respuesta3ds[o].colorbar = window.respuesta3ds[o].canvas.figure.colorbar(surface)
            
            # window.respuesta3ds[o].canvas.axes.view_init(30, 200)
            # window.respuesta3ds[o].canvas.axes.set_xlabel(self.fuzz_inputs[0].label)
            # window.respuesta3ds[o].canvas.axes.set_ylabel(self.fuzz_inputs[1].label)
            # window.respuesta3ds[o].canvas.axes.set_zlabel(self.fuzz_outputs[o].label)
            # window.respuesta3ds[o].canvas.draw() 
