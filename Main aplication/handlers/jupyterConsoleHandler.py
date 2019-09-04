def jupyterConsoleHandler(self):
    base_path = self.resource_path('')
    self.main.jupyterWidget.jupyter_widget._execute("import sys", True)
    self.main.jupyterWidget.jupyter_widget._execute("import copy", True)
    self.main.jupyterWidget.jupyter_widget._execute("sys.path.append(r'" + base_path[:-1] + "')", True)
    self.main.jupyterWidget.jupyter_widget._execute('''for i in copy.deepcopy(sys.path):
                                                           if 'lib' in i and 'Python' in i:
                                                               sys.path.append(i+'\\site-packages')
                                                    ''', True)
