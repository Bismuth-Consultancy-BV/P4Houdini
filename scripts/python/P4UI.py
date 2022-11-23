"""
This is UI code only.
"""

import re
import hou
from hutil.Qt import QtCore, QtGui, QtWidgets


PLUGIN_NAME = "P4Houdini"


def P4Prompt(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(QtGui.QPixmap(hou.text.expandString("$P4HOUDINI/help/icons/perforce-icon.svg")))
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

    value = messagebox.exec()
    if value == QtWidgets.QMessageBox.Ok:
        return True
    return False

def P4ChooseYesNo(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(QtGui.QPixmap(hou.text.expandString("$P4HOUDINI/help/icons/perforce-icon.svg")))
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    value = messagebox.exec()
    if value == QtWidgets.QMessageBox.Yes:
        return True
    return False


def P4Message(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(QtGui.QPixmap(hou.text.expandString("$P4HOUDINI/help/icons/perforce-icon.svg")))
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec()


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def natural_keys_2nd_element(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text[1]) ]

class P4HoudiniChangeListChooser(QtWidgets.QDialog):
    """
    UI for letting user pick the changelist they wish to use.
    """
    def __init__(self, parent, plugin, mode, *args):
        super(P4HoudiniChangeListChooser, self).__init__(parent)
        self.plugin = plugin
        self.mode = mode
        self.proposed_files_to_add = [] if len(args)==0 else args[0]
        self.start_checklist = None if len(args)<2 else args[1]
        self.files_to_add = []
        self.state = False
        self.cl_description = ""
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.selected_changelist = None
        self.available_cl = []
        self.available_cl_id = []

        self.buildUI()
        self.resize(self.minimumSizeHint())

    def closeEvent(self, event):
        pass

    def on_accept(self):
        if self.mode == "submit":
            changelist = self.selected_changelist
            if changelist:
                left = self.listwidget.count()
                for i in range(self.listwidget.count()):
                    item = self.listwidget.item(i)
                    if item.checkState() != QtCore.Qt.Checked:
                        file = item.text().split(" - ")[-1]
                        left -= 1
                        self.plugin.move_file_to_changelist(file, "default")
                if left > 0:
                    self.plugin.set_changelist_description(changelist, self.changelist_desc.toPlainText())
                    self.plugin.submit_changelist(changelist, left)
        elif self.mode == "add":
            to_add = []
            for i in range(self.addwidget.count()):
                item = self.addwidget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    to_add.append(item.text())
            self.files_to_add = to_add
            self.cl_description = self.changelist_desc.toPlainText()
        elif self.mode == "edit":
            self.cl_description = self.changelist_desc.toPlainText()

        self.state = True
        self.close()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.addwidget:
            menu = QtWidgets.QMenu()
            menu.addAction("Make Writeable")
            item = source.itemAt(event.pos())

            if item:
                if menu.exec_(event.globalPos()):
                    file = item.text()
                    self.plugin.make_file_writeable(file)
                    icon = QtGui.QIcon(hou.text.expandString("$P4HOUDINI/misc/p4icons/writeable.png"))
                    item.setIcon(icon)
                    item.setCheckState(QtCore.Qt.Unchecked)

            return True
        return super().eventFilter(source, event)


    def on_cancel(self):
        self.selected_changelist = None
        self.files_to_add = []
        self.state = False
        self.close()

    def construct_changelist_descriptions(self):
        existing = self.plugin.get_pending_changelists()
        added = []
        added_id = []

        if self.mode == "add":
            added.append(self.plugin.preferences["P4CL_Default"])
            added_id.append(self.plugin.preferences["P4CL_Default"])
            added.append("New Changelist...")
            added_id.append(-1)

        for change in existing:
            if change["change"] not in added:
                value = change["change"].strip()
                added_id.append(int(value))
                _desc = change["desc"].strip().split("\n")[0]
                value += " - " + _desc#[:30]
                added.append(value)

        self.available_cl = added
        self.available_cl_id = added_id
        return

    def on_chosen_changelist_changed(self):
        _index = self.changelist_dropdown.currentIndex()
        if _index == -1:
            return
        self.selected_changelist = self.available_cl_id[_index]

        self.update_file_dropdown()
        self.update_cldesc_dropdown()

    def update_cldesc_dropdown(self):
        self.changelist_desc.clear()
        _description = self.plugin.get_description_of_changelist(self.selected_changelist)
        self.changelist_desc.insertPlainText(str(_description))


    def update_file_dropdown(self):
        self.listwidget.clear()
        if isinstance(self.selected_changelist, int):
            changelist = self.selected_changelist
        else:
            changelist = self.plugin.find_changelist_by_description(self.selected_changelist)

        if not changelist or changelist == -1:
            return

        modifications = self.plugin.get_files_in_changelist(changelist)
        modifications.sort(key=natural_keys_2nd_element)


        for action, file, _ in modifications:
            item = QtWidgets.QListWidgetItem()
            item.setText(f"{file}")

            formatting = self.detect_status_submit(action)
            item.setIcon(formatting[0])
            item.setToolTip(formatting[1])

            if self.mode == "submit":
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
            self.listwidget.addItem(item)

    def detect_status_add(self, file):

        icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/empty.png")
        tooltip = ""

        if not self.plugin.preferences["P4CL_Icons"]:
            return [QtGui.QIcon(icon),tooltip]

        if not self.plugin.is_file_registered_in_depot(file):
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/add_self_user.png")
            tooltip = "File marked for add"
            return [QtGui.QIcon(icon),tooltip]

        if not self.plugin.is_file_in_sync(file):
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/unsynced.png")
            tooltip = "A newer version of this file is available"
            return [QtGui.QIcon(icon),tooltip]

        if self.plugin.get_is_checked_out_by_others(file):
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/lock_other_user.png")
            owner = self.plugin.get_owner_of_file(file)
            tooltip = f"File checked out by {owner}"
            return [QtGui.QIcon(icon),tooltip]

        icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/lock_self_user.png")
        tooltip = "File marked for checkout"
        return [QtGui.QIcon(icon),tooltip]

    def detect_status_submit(self, action):
        icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/empty.png")
        tooltip = ""

        if not self.plugin.preferences["P4CL_Icons"]:
            return [QtGui.QIcon(icon),tooltip]

        if action == "add":
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/add_self_user.png")
            tooltip = "File marked for add"
        elif action == "edit":
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/lock_self_user.png")
            tooltip = "File edited"
        elif action == "delete":
            icon = hou.text.expandString("$P4HOUDINI/misc/p4icons/delete.png")
            tooltip = "File marked for delete"
        else:
            print("MISSING ICON FOR", action)

        return [QtGui.QIcon(icon),tooltip]


    def populate_files_to_add_listview(self):
        self.addwidget.clear()

        self.proposed_files_to_add.sort(key=natural_keys)

        for file in self.proposed_files_to_add:
            item = QtWidgets.QListWidgetItem()
            item.setText(f"{file}")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)

            formatting = self.detect_status_add(file)
            item.setIcon(formatting[0])
            item.setToolTip(formatting[1])

            self.addwidget.addItem(item)

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Window title and description
        _window_title = ""
        _window_message = ""
        if self.mode == "add":
            _window_title = PLUGIN_NAME + " - Add or Checkout"
            _window_message = "Select a changelist to add these files to"
        elif self.mode == "submit":
            _window_title = PLUGIN_NAME + " - Submit a Changelist"
            _window_message = "Select a changelist to submit"
        elif self.mode == "edit":
            _window_title = PLUGIN_NAME + " - Edit a Changelist"
            _window_message = "Select a changelist to edit"
        self.setWindowTitle(_window_title)
        message_widget = QtWidgets.QLabel(_window_message)

        if self.mode != "edit":
            layout.addWidget(message_widget)

        # List of files to be added / checked out
        if self.mode == "add":
            self.addwidget = QtWidgets.QListWidget()
            self.populate_files_to_add_listview()
            layout.addWidget(self.addwidget)
            self.addwidget.installEventFilter(self)

        # Changelist picker
        self.changelist_dropdown = QtWidgets.QComboBox(self)
        self.changelist_dropdown.setEditable(False)
        self.construct_changelist_descriptions()
        self.changelist_dropdown.addItems(self.available_cl)
        self.changelist_dropdown.currentIndexChanged.connect(self.on_chosen_changelist_changed)
        layout.addWidget(self.changelist_dropdown)

        # Changelist description
        self.changelist_desc = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.changelist_desc)

        # Changelist overview
        self.listwidget = QtWidgets.QListWidget()
        self.update_file_dropdown()

        layout.addWidget(self.listwidget)

        # Button for the primary action of the dialog
        _main_action_description = ""
        buttonlayout = QtWidgets.QHBoxLayout()
        if self.mode == "add":
            _main_action_description = "Add"
        elif self.mode == "submit":
            _main_action_description = "Submit"
        elif self.mode == "edit":
            _main_action_description = "Apply"
        self.update_button = QtWidgets.QPushButton(_main_action_description)
        self.update_button.clicked.connect(self.on_accept)
        buttonlayout.addWidget(self.update_button)

        # Button for canceling
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        buttonlayout.addWidget(self.cancel_button)

        layout.addLayout(buttonlayout)

        if self.mode == "edit":
            _index = self.available_cl_id.index(int(self.start_checklist))
            self.changelist_dropdown.setCurrentIndex(_index)

        self.on_chosen_changelist_changed()
        if self.mode == "add":
            self.setMinimumSize(hou.ui.scaledSize(700),
            hou.ui.scaledSize(400))
        else:
            self.setMinimumSize(hou.ui.scaledSize(700),
            hou.ui.scaledSize(400))
