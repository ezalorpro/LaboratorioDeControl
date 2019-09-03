from PySide2.QtWidgets import QWidget, QGraphicsView
from PySide2.QtWidgets import QVBoxLayout
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager


class JupyterConsole(QGraphicsView):

    def __init__(self, parent=None):
        super(JupyterConsole, self).__init__(parent)
        self.kernel_manager = QtKernelManager(kernel_name='python3')
        self.kernel_manager.start_kernel()

        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

        self.jupyter_widget = RichJupyterWidget()
        self.jupyter_widget.kernel_manager = self.kernel_manager
        self.jupyter_widget.kernel_client = self.kernel_client
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.jupyter_widget)
        self.setLayout(vertical_layout)

        self.jupyter_widget._execute("import sys", True)
        self.jupyter_widget._execute(
            "sys.path.append(r'c:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication')",
            True)

        # self.jupyter_widget._execute(
        #     "sys.path.append('c:/Users/PC/Documents/Descargas chrome/NO TOCAR MALDITO IDIOTA!! ZZZZ/kleiver/Tesis/Nueva tesis/LaboratorioDeControl/Main aplication')",
        #     True)
