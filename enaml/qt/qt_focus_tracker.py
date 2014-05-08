#------------------------------------------------------------------------------
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from enaml.widgets.focus_tracker import ProxyFocusTracker

from .QtGui import QApplication

from .qt_toolkit_object import QtToolkitObject


class QtFocusTracker(QtToolkitObject, ProxyFocusTracker):
    """ A Qt implementation of an Enaml ProxyFocusTracker.

    """
    def create_widget(self):
        """ Create the underlying widget.

        """
        # A focus tracker does not have a widget representation.
        self.widget = None

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(QtFocusTracker, self).init_widget()
        QApplication.instance().focusChanged.connect(self._on_focus_changed)
        self._update_focus_widget()

    def destroy(self):
        """ A reimplemented destructor.

        """
        QApplication.instance().focusChanged.disconnect(self._on_focus_changed)
        super(QtFocusTracker, self).destroy()

    def _on_focus_changed(self, old, new):
        """ Handle the application 'focusChanged' signal.

        """
        self._update_focus_widget()

    def _update_focus_widget(self):
        """ Update the tracker with currently focused widget.

        """
        fw = QApplication.focusWidget()
        fp = fw and getattr(fw, '_d_proxy', None)
        fd = fp and fp.declaration
        self.declaration.focused_widget = fd