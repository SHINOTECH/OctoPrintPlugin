from UM.i18n import i18nCatalog
from cura.MachineAction import MachineAction
import cura.CuraContainerRegistry

from UM.Settings.DefinitionContainer import DefinitionContainer

from UM.Application import Application

from PyQt5.QtCore import pyqtSignal, pyqtProperty, pyqtSlot, QObject

catalog = i18nCatalog("cura")

class DiscoverOctoPrintAction(MachineAction, QObject, ):
    def __init__(self, parent = None):
        MachineAction.__init__(self, "DiscoverOctoPrintAction", catalog.i18nc("@action","Connect OctoPrint"))

        self._qml_url = "DiscoverOctoPrintAction.qml"
        self._window = None
        self._context = None

        self._network_plugin = None

        cura.CuraContainerRegistry.CuraContainerRegistry.getInstance().containerAdded.connect(self._onContainerAdded)

    printerDetected = pyqtSignal()

    @pyqtSlot()
    def startDiscovery(self):
        if not self._network_plugin:
            self._network_plugin = Application.getInstance().getOutputDeviceManager().getOutputDevicePlugin("OctoPrintPlugin")
            self._network_plugin.addPrinterSignal.connect(self._onPrinterAdded)
            self.printerDetected.emit()

    def _onPrinterAdded(self, *args):
        self.printerDetected.emit()

    def _onContainerAdded(self, container):
        # Add this action as a supported action to all machine definitions
        if isinstance(container, DefinitionContainer) and container.getMetaDataEntry("type") == "machine":
            Application.getInstance().getMachineActionManager().addSupportedAction(container.getId(), self.getKey())

    @pyqtProperty("QVariantList", notify = printerDetected)
    def foundDevices(self):
        if self._network_plugin:
            printers = self._network_plugin.getPrinters()
            return [printers[printer] for printer in printers]
        else:
            return []

    @pyqtSlot(str)
    def setKey(self, key):
        global_container_stack = Application.getInstance().getGlobalContainerStack()
        if global_container_stack:
            if "octoprint_id" in global_container_stack.getMetaData():
                global_container_stack.setMetaDataEntry("octoprint_id", key)
            else:
                global_container_stack.addMetaDataEntry("octoprint_id", key)

        if self._network_plugin:
            # Ensure that the connection states are refreshed.
            self._network_plugin.reCheckConnections()

    @pyqtSlot(str)
    def setApiKey(self, api_key):
        global_container_stack = Application.getInstance().getGlobalContainerStack()
        if global_container_stack:
            if "octoprint_api_key" in global_container_stack.getMetaData():
                global_container_stack.setMetaDataEntry("octoprint_api_key", api_key)
            else:
                global_container_stack.addMetaDataEntry("octoprint_api_key", api_key)

        if self._network_plugin:
            # Ensure that the connection states are refreshed.
            self._network_plugin.reCheckConnections()

    ##  Get the stored API key of this machine
    #   \return key String containing the key of the machine.
    @pyqtProperty(str)
    def apiKey(self):
        global_container_stack = Application.getInstance().getGlobalContainerStack()
        if global_container_stack:
            return global_container_stack.getMetaDataEntry("octoprint_api_key")
        else:
            return ""
