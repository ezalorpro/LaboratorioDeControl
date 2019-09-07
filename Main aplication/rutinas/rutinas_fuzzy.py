import numpy as np
from skfuzzymdf import control as fuzz
from skfuzzymdf.membership import generatemf
from skfuzzymdf.control.visualization import FuzzyVariableVisualizer
from skfuzzymdf.control.controlsystem import CrispValueCalculator
from skfuzzymdf.fuzzymath.fuzzy_ops import interp_membership
from collections import OrderedDict
from matplotlib import pyplot as plt
from parse import parse
# import pyvista as pv
import ast
import pyqtgraphmdf as pg
import copy
import json
import re


class FuzzyController:

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
            temp_in = fuzz.Antecedent(np.linspace(*ins['rango'], 200), ins['nombre'])
            vector.append(temp_in)
        return vector

    def crear_output(self, outputlist):
        vector = []
        for i, ins in enumerate(outputlist):
            temp_in = fuzz.Consequent(np.linspace(*ins['rango'], 200),
                                      ins['nombre'],
                                      ins['metodo'])
            vector.append(temp_in)
        return vector

    def crear_etiquetas_input(self, inputlist):

        for n, i in enumerate(inputlist):
            for eti in i['etiquetas']:
                self.fuzz_inputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(
                    self.fuzz_inputs[n].universe, *eti['definicion'])

    def crear_etiquetas_output(self, outputlist):
        for n, i in enumerate(outputlist):
            for eti in i['etiquetas']:
                self.fuzz_outputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(
                    self.fuzz_outputs[n].universe, *eti['definicion'])

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
        self.fuzz_inputs[i].universe = np.asarray(np.linspace(*inputlist[i]['rango'],
                                                              200))
        self.graficar_mf_in(window, i)

    def update_rango_output(self, window, outputlist, o):
        self.fuzz_outputs[o].universe = np.asarray(
            np.linspace(*outputlist[o]['rango'], 200))
        self.graficar_mf_out(window, o)

    def cambiar_metodo(self, window, o, metodo):
        self.fuzz_inputs[o].defuzzify_method = metodo

    def cambio_etinombre_input(self, window, inputlist, i, n, old_name):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i].terms.pop(old_name)
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(
            self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)

    def cambio_etinombre_output(self, window, outputlist, o, n, old_name):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o].terms.pop(old_name)
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(
            self.fuzz_outputs[o].universe, *eti['definicion'])
        self.graficar_mf_out(window, o)

    def update_definicion_input(self, window, inputlist, i, n):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(
            self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)

    def update_definicion_output(self, window, outputlist, o, n):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(
            self.fuzz_outputs[o].universe, *eti['definicion'])
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

            self.rulelist[
                -1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni] % weight_ini

            for i in Etiquetasin[1:len(Etiquetasin)]:
                if logica:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[
                            -1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[
                            -1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
                else:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[
                            -1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[
                            -1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]

            for o in Etiquetasout[1:len(Etiquetasout)]:
                self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]] % o[2])

        return self.rulelist

    def agregar_regla(self, window, ni, no, Etiquetasin, Etiquetasout):

        self.rulelist.append(fuzz.Rule())

        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]

        if not negacion_ini:
            self.rulelist[-1].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
        else:
            self.rulelist[-1].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]

        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]

        self.rulelist[
            -1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni] % weight_ini

        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[
                        -1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[
                        -1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[
                        -1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[
                        -1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]

        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]] % o[2])

        return self.rulelist[-1]

    def eliminar_regla(self, index_rule):
        del self.rulelist[index_rule]

    def cambiar_regla(self, window, ni, no, Etiquetasin, Etiquetasout, index_rule):
        del self.rulelist[index_rule]
        self.rulelist.insert(index_rule, fuzz.Rule())

        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]

        if not negacion_ini:
            self.rulelist[index_rule].antecedent = self.fuzz_inputs[ni_ini][
                inetiqueta_ini]
        else:
            self.rulelist[
                index_rule].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]

        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]

        self.rulelist[index_rule].consequent = self.fuzz_outputs[no_ini][
            outetiqueta_oni] % weight_ini

        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[
                        index_rule].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[
                        index_rule].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[
                        index_rule].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[
                        index_rule].antecedent | ~self.fuzz_inputs[i[1]][i[0]]

        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[index_rule].consequent.append(self.fuzz_outputs[o[1]][o[0]] %
                                                        o[2])

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
            FuzzyVariableVisualizer(self.fuzz_inputs[i], grafica,
                                    grafica.canvas.axes).view_gui(self.Controlador,
                                                                  legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()

        for o, grafica in enumerate(window.outgraphs[:no]):
            grafica.canvas.axes.clear()
            value = FuzzyVariableVisualizer(self.fuzz_outputs[o],
                                            grafica,
                                            grafica.canvas.axes).view_gui(
                                                self.Controlador, legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()

            window.outtestlabels[o].setText(window.OutputList[o]['nombre'] +
                                            f': {np.around(value, 3)}')

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
                entradas.append(window.ingraphs[i].plotwidget.plot(
                    self.fuzz_inputs[i].universe,
                    term.mf,
                    pen={
                        'width': 2, 'color': pg.mkColor(self.colors[color])
                    }))

                under_plot = window.ingraphs[i].plotwidget.plot(
                    ups_universe,
                    zeros,
                    pen={
                        'width': 0.1, 'color': pg.mkColor(self.colors[color] + '6A')
                    })

                over_plot = window.ingraphs[i].plotwidget.plot(
                    ups_universe,
                    cut_mfs[key],
                    pen={
                        'width': 0.1, 'color': pg.mkColor(self.colors[color] + '6A')
                    })

                fillItem = pg.FillBetweenItem(under_plot,
                                              over_plot,
                                              brush=pg.mkColor(self.colors[color] + '6A'))

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
                            y = max(
                                y,
                                interp_membership(self.fuzz_inputs[i].universe,
                                                  term.mf,
                                                  crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    crispPlot = window.ingraphs[i].plotwidget.plot([crisp_value] * 2,
                                                                   np.asarray([0, y]),
                                                                   pen={
                                                                       'width': 6,
                                                                       'color': 'k'
                                                                   })

                else:
                    crisp_value = 0
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
                salidas.append(window.outgraphs[i].plotwidget.plot(
                    self.fuzz_outputs[i].universe,
                    term.mf,
                    pen={
                        'width': 2, 'color': pg.mkColor(self.colors[color])
                    }))

                under_plot = window.outgraphs[i].plotwidget.plot(
                    ups_universe,
                    zeros,
                    pen={
                        'width': 0.1, 'color': pg.mkColor(self.colors[color] + '6A')
                    })

                over_plot = window.outgraphs[i].plotwidget.plot(
                    ups_universe,
                    cut_mfs[key],
                    pen={
                        'width': 0.1, 'color': pg.mkColor(self.colors[color] + '6A')
                    })

                fillItem = pg.FillBetweenItem(under_plot,
                                              over_plot,
                                              brush=pg.mkColor(self.colors[color] + '6A'))

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
                            y = max(
                                y,
                                interp_membership(self.fuzz_outputs[i].universe,
                                                  term.mf,
                                                  crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    crispPlot = window.outgraphs[i].plotwidget.plot([crisp_value] * 2,
                                                                    np.asarray([0, y]),
                                                                    pen={
                                                                        'width': 6,
                                                                        'color': 'k'
                                                                    })

                else:
                    crisp_value = 0
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
                self.inlabelsplot[i][etiq].setData(
                    self.fuzz_inputs[i].universe,
                    self.fuzz_inputs[i].terms[label['nombre']].mf)
                under_plot, over_plot = self.inareas[i][etiq]
                under_plot.setData(ups_universe, zeros)
                over_plot.setData(ups_universe, cut_mfs[label['nombre']])

            if len(cut_mfs) > 0 and not all(output_mf == 0):
                crisp_value = self.fuzz_inputs[i].input[self.Controlador]
                if crisp_value is not None:
                    y = 0.
                    for key, term in self.fuzz_inputs[i].terms.items():
                        if key in cut_mfs:
                            y = max(
                                y,
                                interp_membership(self.fuzz_inputs[i].universe,
                                                  term.mf,
                                                  crisp_value))
                    if y < 0.1:
                        y = 1.

                    self.invalues[i].setData([crisp_value] * 2, np.asarray([0, y]))
                else:
                    crisp_value = 0
            else:
                crisp_value = 0

        for i in range(no):
            crispy = CrispValueCalculator(self.fuzz_outputs[i], self.Controlador)
            ups_universe, output_mf, cut_mfs = crispy.find_memberships()
            zeros = np.zeros_like(ups_universe, dtype=np.float64)

            for etiq, label in enumerate(window.OutputList[i]['etiquetas']):
                self.outlabelsplot[i][etiq].setData(
                    self.fuzz_outputs[i].universe,
                    self.fuzz_outputs[i].terms[label['nombre']].mf)
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
                            y = max(
                                y,
                                interp_membership(self.fuzz_outputs[i].universe,
                                                  term.mf,
                                                  crisp_value))

                    # Small cut values are hard to see, so simply set them to 1
                    if y < 0.1:
                        y = 1.

                    self.outvalues[i].setData([crisp_value] * 2, np.asarray([0, y]))

                else:
                    crisp_value = 0
            else:
                crisp_value = 0

            window.outtestlabels[i].setText(window.OutputList[i]['nombre'] +
                                            f': {np.around(crisp_value, 3)}')

    def graficar_respuesta_2d(self, window, inrange, no):
        entrada = np.linspace(*inrange, 500)

        entradas = []
        salidas = [[] for i in range(no)]

        for value in entrada:
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
        n_puntos = 25
        entrada1 = np.linspace(*inrange1, n_puntos)
        entrada2 = np.linspace(*inrange2, n_puntos)
        entrada1, entrada2 = np.meshgrid(entrada1, entrada2)

        entrada11 = [np.zeros_like(entrada1) for i in range(no)]
        entrada22 = [np.zeros_like(entrada2) for i in range(no)]

        salidas = [np.zeros_like(entrada1) for i in range(no)]

        for i in range(n_puntos):
            for j in range(n_puntos):
                self.Controlador.input[self.fuzz_inputs[0].label] = entrada1[i, j]
                self.Controlador.input[self.fuzz_inputs[1].label] = entrada2[i, j]
                try:
                    self.Controlador.compute()
                    for o in range(no):
                        entrada11[o][i, j] = entrada1[i, j]
                        entrada22[o][i, j] = entrada2[i, j]
                        salidas[o][i, j] = self.Controlador.output[
                            self.fuzz_outputs[o].label]
                except:
                    pass

        for o in range(no):
            window.respuesta3ds[o].canvas.axes.clear()

            if window.respuesta3ds[o].colorbar != 0:
                window.respuesta3ds[o].colorbar.remove()

            surface = window.respuesta3ds[o].canvas.axes.plot_surface(entrada11[o], entrada22[o], salidas[o],
                                                            rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)

            window.respuesta3ds[o].colorbar = window.respuesta3ds[o].canvas.figure.colorbar(surface)

            window.respuesta3ds[o].canvas.axes.view_init(30, 200)
            window.respuesta3ds[o].canvas.axes.set_xlabel(self.fuzz_inputs[0].label)
            window.respuesta3ds[o].canvas.axes.set_ylabel(self.fuzz_inputs[1].label)
            window.respuesta3ds[o].canvas.axes.set_zlabel(self.fuzz_outputs[o].label)
            window.respuesta3ds[o].canvas.draw()

        # for o in range(no):

        #     x = copy.deepcopy(entrada11[o])
        #     y = copy.deepcopy(entrada22[o])
        #     z = copy.deepcopy(salidas[o])

        #     window.respuesta3ds[o].vtk_widget.clear()
        #     window.respuesta3ds[o].vtk_widget.remove_bounds_axes()

        #     xscale = (np.max(z) - np.min(z)) / (np.max(x) - np.min(x))
        #     yscale = (np.max(z) - np.min(z)) / (np.max(y) - np.min(y))

        #     window.respuesta3ds[o].vtk_widget.set_scale(xscale=xscale, yscale=yscale)

        #     grid = pv.StructuredGrid(x, y, z)
        #     grid['scalars'] = z.ravel('F')

        #     window.respuesta3ds[o].vtk_widget.add_mesh(grid,
        #                                                scalars='scalars',
        #                                                cmap='viridis',
        #                                                style='surface',
        #                                                lighting=False,
        #                                                show_edges=True,
        #                                                stitle=self.fuzz_outputs[o].label,
        #                                                scalar_bar_args={
        #                                                    'label_font_size': 18,
        #                                                    'title_font_size': 18,
        #                                                    'position_x': 0.99
        #                                                })

        #     window.respuesta3ds[o].vtk_widget.show_bounds(
        #         grid='True',
        #         location='outer',
        #         ticks='inside',
        #         xlabel=self.fuzz_inputs[0].label,
        #         ylabel=self.fuzz_inputs[1].label,
        #         zlabel=self.fuzz_outputs[o].label,
        #         padding=0.1,
        #         use_2d=True,
        #         font_size=12,
        #         bounds=[np.min(x), np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)])

        #     window.respuesta3ds[o].vtk_widget.show_axes()
        #     window.respuesta3ds[o].vtk_widget.reset_camera()
        #     window.respuesta3ds[o].vtk_widget.update()

    def calcular_valor(self, inputs, outputs):
        for i, value in enumerate(inputs):
            value = np.clip(value, np.min(self.fuzz_inputs[i].universe), np.max(self.fuzz_inputs[i].universe))
            self.Controlador.input[self.fuzz_inputs[i].label] = value

        self.Controlador.compute()

        for o in range(len(outputs)):
            outputs[o] = self.Controlador.output[self.fuzz_outputs[o].label]

        return outputs


class FISParser:

    def __init__(self, file, InputList=None, OutputList=None, RuleEtiquetas=None):
        if InputList is None and OutputList is None and RuleEtiquetas is None:
            with open(file, 'r') as infis:
                self.rawlines = infis.readlines()
            self.systemList = 0
            self.InputList = []
            self.OutputList = []
            self.RuleList = []
            self.get_system()
            self.get_vars()
            self.get_rules()
        else:
            self.file = file
            self.InputList = InputList
            self.OutputList = OutputList
            self.RuleEtiquetas = RuleEtiquetas
            self.json_to_fis()

    def get_system(self):
        end_sysblock = self.rawlines.index('\n')
        systemblock = self.rawlines[1:end_sysblock]
        fisargs = map(lambda x: parse('{arg}={val}', x), systemblock)
        fissys = {f['arg'].lower(): f['val'].strip("'") for f in fisargs}
        self.numinputs = int(fissys['numinputs'])
        self.numoutputs = int(fissys['numoutputs'])
        self.numrules = int(fissys['numrules'])
        self.start_varblocks = end_sysblock + 1
        self.systemList = fissys

    def get_var(self, vartype, varnum, start_line, end_line):
        varblock = self.rawlines[start_line:end_line]
        fisargs = map(lambda x: parse('{arg}={val}', x), varblock)
        fisvar = {f['arg'].lower(): f['val'].strip("'") for f in fisargs}

        if 'input' in vartype:
            self.InputList.append(fisvar)
        elif 'output' in vartype:
            self.OutputList.append(fisvar)

    def get_vars(self):
        start_ruleblock = self.rawlines.index('[Rules]\n')
        var_lines = []
        var_types = []
        flag = 0
        for i, line in enumerate(self.rawlines[self.start_varblocks - 1:start_ruleblock]):
            if flag:
                flag = 0
                vt = parse('[{type}{num:d}]', line)
                var_types.append((vt['type'].lower(), vt['num']))
            if line == '\n':
                var_lines.append(i + self.start_varblocks - 1)
                flag = 1
        for i, l in enumerate(var_lines[:-1]):
            if 'input' in var_types[i][0]:
                self.get_var('input', var_types[i][1] - 1, l + 2, var_lines[i + 1])
            elif 'output' in var_types[i][0]:
                self.get_var('output', var_types[i][1] - 1, l + 2, var_lines[i + 1])

    def get_rules(self):
        start_ruleblock = self.rawlines.index('[Rules]\n')
        ruleblock = self.rawlines[start_ruleblock + 1:]
        antecedents = (('{a%d:d} ' * self.numinputs) %
                       tuple(range(self.numinputs))).strip()
        consequents = ('{c%d:d} ' * self.numoutputs) % tuple(range(self.numoutputs))
        p = antecedents + ', ' + consequents + '({w:d}) : {c:d}'
        for rule in ruleblock:
            try:
                p = antecedents + ', ' + consequents + '({w:d}) : {c:d}'
                rp = parse(p, rule)
                r = []
                for inp in range(self.numinputs):
                    rpar = rp['a%d' % inp]
                    rval = rpar if rpar != 0 else None
                    r.append(rval)
                for outp in range(self.numoutputs):
                    rpar = rp['c%d' % outp]
                    rval = rpar if rpar != 0 else None
                    r.append(rval)
                r += [rp['w'], rp['c'] - 1]
                self.RuleList.append(r)
            except:
                p = antecedents + ', ' + consequents + '({w:f}) : {c:d}'
                rp = parse(p, rule)
                r = []
                for inp in range(self.numinputs):
                    rpar = rp['a%d' % inp]
                    rval = rpar if rpar != 0 else None
                    r.append(rval)
                for outp in range(self.numoutputs):
                    rpar = rp['c%d' % outp]
                    rval = rpar if rpar != 0 else None
                    r.append(rval)
                r += [rp['w'], rp['c'] - 1]
                self.RuleList.append(r)

    def fis_to_json(self):
        ni = int(self.systemList['numinputs'])
        no = int(self.systemList['numoutputs'])
        nr = int(self.systemList['numrules'])

        InputList = [0] * ni
        OutputList = [0] * no
        RuleEtiquetas = []

        for i in range(ni):
            InputList[i] = {
                "nombre":
                    self.InputList[i]['name'],
                "numeroE":
                    int(self.InputList[i]['nummfs']),
                "etiquetas": [0] * int(self.InputList[i]['nummfs']),
                "rango":
                    ast.literal_eval(
                        re.sub("\s+", ",", self.InputList[i]['range'].strip()))
            }

            for ne in range(int(self.InputList[i]['nummfs'])):
                temp_etiqueta = self.InputList[0]['mf' + str(ne + 1)].replace(
                    "'", '').split(':')
                temp2 = temp_etiqueta[1].split(',')
                InputList[i]['etiquetas'][ne] = {
                    "nombre": temp_etiqueta[0],
                    "mf": temp2[0],
                    "definicion": ast.literal_eval(re.sub("\s+", ",", temp2[1].strip()))
                }

        for i in range(no):
            OutputList[i] = {
                "nombre":
                    self.OutputList[i]['name'],
                "numeroE":
                    int(self.OutputList[i]['nummfs']),
                "etiquetas": [0] * int(self.OutputList[i]['nummfs']),
                "rango":
                    ast.literal_eval(
                        re.sub("\s+", ",", self.OutputList[i]['range'].strip())),
                "metodo":
                    self.systemList['defuzzmethod']
            }

            for ne in range(int(self.OutputList[i]['nummfs'])):
                temp_etiqueta = self.OutputList[i]['mf' + str(ne + 1)].replace(
                    "'", '').split(':')
                temp2 = temp_etiqueta[1].split(',')
                OutputList[i]['etiquetas'][ne] = {
                    "nombre": temp_etiqueta[0],
                    "mf": temp2[0],
                    "definicion": ast.literal_eval(re.sub("\s+", ",", temp2[1].strip()))
                }
        for numeror, i in enumerate(self.RuleList):
            ril = []
            rol = []

            for j in range(ni):
                if i[j] is not None:
                    nombre = InputList[j]['etiquetas'][abs(i[j]) - 1]['nombre']
                    numero = j
                    negacion = False if i[j] > 0 else True
                    ril.append([nombre, numero, negacion])

            for j in range(ni, no + ni):
                if i[j] is not None:
                    if i[j] < 0:
                        raise TypeError('No se permiten salidas negadas')
                    nombre = OutputList[j - ni]['etiquetas'][abs(i[j]) - 1]['nombre']
                    numero = j - ni
                    peso = float(i[no + ni])
                    rol.append([nombre, numero, peso])

            and_condition = True if i[ni + no + 1] == 0 else False
            RuleEtiquetas.append(copy.deepcopy([ril, rol, and_condition]))

        return copy.deepcopy(InputList), copy.deepcopy(OutputList), copy.deepcopy(RuleEtiquetas)

    def json_to_fis(self):
        ni = len(self.InputList)
        no = len(self.OutputList)
        nr = len(self.RuleEtiquetas)

        with open(self.file, 'w') as f:
            f.write(f"[System]\n")
            f.write(f"Name='{self.file.split('/')[-1].split('.')[0]}'\n")
            f.write(f"Type='mamdani'\n")
            f.write(f"Version=2.0\n")
            f.write(f"NumInputs={ni}\n")
            f.write(f"NumOutputs={no}\n")
            f.write(f"NumRules={nr}\n")
            f.write(f"AndMethod='min'\n")
            f.write(f"OrMethod='max'\n")
            f.write(f"ImpMethod='min'\n")
            f.write(f"AggMethod='max'\n")
            f.write(f"DefuzzMethod='{self.OutputList[0]['metodo']}'\n")
            f.write(f"\n")

            for i in range(ni):
                f.write(f"[Input" + str(i + 1) + "]\n")
                f.write(f"Name='{self.InputList[i]['nombre']}'\n")
                string_temp = re.sub('\s+', '',
                                     str(self.InputList[i]['rango'])).replace(',', ' ')
                f.write(f"Range={string_temp}\n")
                f.write(f"NumMFs={self.InputList[i]['numeroE']}\n")

                for ne in range(self.InputList[i]['numeroE']):
                    string_temp = re.sub(
                        '\s+', '',
                        str(self.InputList[i]['etiquetas'][ne]['definicion'])).replace(
                            ',', ' ')
                    f.write(
                        f"MF{ne+1}='{self.InputList[i]['etiquetas'][ne]['nombre']}':'{self.InputList[i]['etiquetas'][ne]['mf']}',{string_temp}\n"
                    )

                f.write(f"\n")

            for i in range(no):
                f.write(f"[Output" + str(i + 1) + "]\n")
                f.write(f"Name='{self.OutputList[i]['nombre']}'\n")
                string_temp = re.sub('\s+', '',
                                     str(self.OutputList[i]['rango'])).replace(',', ' ')
                f.write(f"Range={string_temp}\n")
                f.write(f"NumMFs={self.OutputList[i]['numeroE']}\n")

                for ne in range(self.OutputList[i]['numeroE']):
                    string_temp = re.sub(
                        '\s+', '',
                        str(self.OutputList[i]['etiquetas'][ne]['definicion'])).replace(
                            ',', ' ')
                    f.write(
                        f"MF{ne+1}='{self.OutputList[i]['etiquetas'][ne]['nombre']}':'{self.OutputList[i]['etiquetas'][ne]['mf']}',{string_temp}\n"
                    )

                f.write(f"\n")

            rules_no_format = []
            for i, rule in enumerate(self.RuleEtiquetas):

                inner_rules = []
                for nir in range(ni):
                    for inputrule in rule[0]:
                        if nir == inputrule[1]:
                            if not inputrule[2]:
                                for ner, etiqueta in enumerate(self.InputList[nir]['etiquetas']):
                                    if etiqueta['nombre'] == inputrule[0]:
                                        inner_rules.append(ner + 1)
                                        break
                            else:
                                for ner, etiqueta in enumerate(self.InputList[nir]['etiquetas']):
                                    if etiqueta['nombre'] == inputrule[0]:
                                        inner_rules.append(-ner - 1)
                                        break

                            break
                        else:
                            continue
                    else:
                        inner_rules.append(0)
                        break

                for nor in range(no):
                    for outputtrule in rule[1]:
                        if nor == outputtrule[1]:
                            for ner, etiqueta in enumerate(self.OutputList[nor]['etiquetas']):
                                if etiqueta['nombre'] == outputtrule[0]:
                                    inner_rules.append(ner + 1)
                                    break
                            break
                        else:
                            continue
                    else:
                        inner_rules.append(0)

                inner_rules.append(rule[1][0][2])

                if rule[2]:
                    inner_rules.append(1)
                else:
                    inner_rules.append(2)

                rules_no_format.append(copy.deepcopy(inner_rules))

            f.write(f"[Rules]\n")

            for i in range(nr):
                rule_str = ""
                for j in range(ni):
                    rule_str += str(rules_no_format[i][j]) + " "
                rule_str += ","
                for j in range(ni, ni + no):
                    rule_str += str(rules_no_format[i][j]) + " "
                rule_str += f"({str(rules_no_format[i][ni+no])})" + " "
                rule_str += f": {str(rules_no_format[i][ni+no+1])}\n"
                f.write(rule_str)
