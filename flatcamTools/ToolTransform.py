############################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# http://flatcam.org                                       #
# File Author: Marius Adrian Stanciu (c)                   #
# Date: 3/10/2019                                          #
# MIT Licence                                              #
############################################################

from FlatCAMTool import FlatCAMTool
from FlatCAMObj import *

import gettext
import FlatCAMTranslation as fcTranslate

fcTranslate.apply_language('ToolTransform')
import builtins
if '_' not in builtins.__dict__:
    _ = gettext.gettext


class ToolTransform(FlatCAMTool):

    toolName = _("Object Transform")
    rotateName = _("Rotate")
    skewName = _("Skew/Shear")
    scaleName = _("Scale")
    flipName = _("Mirror (Flip)")
    offsetName = _("Offset")

    def __init__(self, app):
        FlatCAMTool.__init__(self, app)

        self.transform_lay = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.transform_lay)
        ## Title
        title_label = QtWidgets.QLabel("%s" % self.toolName)
        title_label.setStyleSheet("""
                        QLabel
                        {
                            font-size: 16px;
                            font-weight: bold;
                        }
                        """)
        self.transform_lay.addWidget(title_label)

        self.empty_label = QtWidgets.QLabel("")
        self.empty_label.setFixedWidth(50)

        self.empty_label1 = QtWidgets.QLabel("")
        self.empty_label1.setFixedWidth(70)
        self.empty_label2 = QtWidgets.QLabel("")
        self.empty_label2.setFixedWidth(70)
        self.empty_label3 = QtWidgets.QLabel("")
        self.empty_label3.setFixedWidth(70)
        self.empty_label4 = QtWidgets.QLabel("")
        self.empty_label4.setFixedWidth(70)
        self.transform_lay.addWidget(self.empty_label)

        ## Rotate Title
        rotate_title_label = QtWidgets.QLabel("<font size=3><b>%s</b></font>" % self.rotateName)
        self.transform_lay.addWidget(rotate_title_label)

        ## Layout
        form_layout = QtWidgets.QFormLayout()
        self.transform_lay.addLayout(form_layout)
        form_child = QtWidgets.QHBoxLayout()

        self.rotate_label = QtWidgets.QLabel(_("Angle:"))
        self.rotate_label.setToolTip(
            _("Angle for Rotation action, in degrees.\n"
            "Float number between -360 and 359.\n"
            "Positive numbers for CW motion.\n"
            "Negative numbers for CCW motion.")
        )
        self.rotate_label.setFixedWidth(50)

        self.rotate_entry = FCEntry()
        # self.rotate_entry.setFixedWidth(60)
        self.rotate_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.rotate_button = FCButton()
        self.rotate_button.set_value(_("Rotate"))
        self.rotate_button.setToolTip(
            _("Rotate the selected object(s).\n"
            "The point of reference is the middle of\n"
            "the bounding box for all selected objects.")
        )
        self.rotate_button.setFixedWidth(60)

        form_child.addWidget(self.rotate_entry)
        form_child.addWidget(self.rotate_button)

        form_layout.addRow(self.rotate_label, form_child)

        self.transform_lay.addWidget(self.empty_label1)

        ## Skew Title
        skew_title_label = QtWidgets.QLabel("<font size=3><b>%s</b></font>" % self.skewName)
        self.transform_lay.addWidget(skew_title_label)

        ## Form Layout
        form1_layout = QtWidgets.QFormLayout()
        self.transform_lay.addLayout(form1_layout)
        form1_child_1 = QtWidgets.QHBoxLayout()
        form1_child_2 = QtWidgets.QHBoxLayout()

        self.skewx_label = QtWidgets.QLabel(_("Angle X:"))
        self.skewx_label.setToolTip(
            _("Angle for Skew action, in degrees.\n"
            "Float number between -360 and 359.")
        )
        self.skewx_label.setFixedWidth(50)
        self.skewx_entry = FCEntry()
        self.skewx_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.skewx_entry.setFixedWidth(60)

        self.skewx_button = FCButton()
        self.skewx_button.set_value(_("Skew X"))
        self.skewx_button.setToolTip(
            _("Skew/shear the selected object(s).\n"
            "The point of reference is the middle of\n"
            "the bounding box for all selected objects."))
        self.skewx_button.setFixedWidth(60)

        self.skewy_label = QtWidgets.QLabel(_("Angle Y:"))
        self.skewy_label.setToolTip(
            _("Angle for Skew action, in degrees.\n"
            "Float number between -360 and 359.")
        )
        self.skewy_label.setFixedWidth(50)
        self.skewy_entry = FCEntry()
        self.skewy_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.skewy_entry.setFixedWidth(60)

        self.skewy_button = FCButton()
        self.skewy_button.set_value(_("Skew Y"))
        self.skewy_button.setToolTip(
            _("Skew/shear the selected object(s).\n"
            "The point of reference is the middle of\n"
            "the bounding box for all selected objects."))
        self.skewy_button.setFixedWidth(60)

        form1_child_1.addWidget(self.skewx_entry)
        form1_child_1.addWidget(self.skewx_button)

        form1_child_2.addWidget(self.skewy_entry)
        form1_child_2.addWidget(self.skewy_button)

        form1_layout.addRow(self.skewx_label, form1_child_1)
        form1_layout.addRow(self.skewy_label, form1_child_2)

        self.transform_lay.addWidget(self.empty_label2)

        ## Scale Title
        scale_title_label = QtWidgets.QLabel("<font size=3><b>%s</b></font>" % self.scaleName)
        self.transform_lay.addWidget(scale_title_label)

        ## Form Layout
        form2_layout = QtWidgets.QFormLayout()
        self.transform_lay.addLayout(form2_layout)
        form2_child_1 = QtWidgets.QHBoxLayout()
        form2_child_2 = QtWidgets.QHBoxLayout()

        self.scalex_label = QtWidgets.QLabel(_("Factor X:"))
        self.scalex_label.setToolTip(
            _("Factor for Scale action over X axis.")
        )
        self.scalex_label.setFixedWidth(50)
        self.scalex_entry = FCEntry()
        self.scalex_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.scalex_entry.setFixedWidth(60)

        self.scalex_button = FCButton()
        self.scalex_button.set_value(_("Scale X"))
        self.scalex_button.setToolTip(
            _("Scale the selected object(s).\n"
            "The point of reference depends on \n"
            "the Scale reference checkbox state."))
        self.scalex_button.setFixedWidth(60)

        self.scaley_label = QtWidgets.QLabel(_("Factor Y:"))
        self.scaley_label.setToolTip(
            _("Factor for Scale action over Y axis.")
        )
        self.scaley_label.setFixedWidth(50)
        self.scaley_entry = FCEntry()
        self.scaley_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.scaley_entry.setFixedWidth(60)

        self.scaley_button = FCButton()
        self.scaley_button.set_value(_("Scale Y"))
        self.scaley_button.setToolTip(
            _("Scale the selected object(s).\n"
            "The point of reference depends on \n"
            "the Scale reference checkbox state."))
        self.scaley_button.setFixedWidth(60)

        self.scale_link_cb = FCCheckBox()
        self.scale_link_cb.set_value(True)
        self.scale_link_cb.setText(_("Link"))
        self.scale_link_cb.setToolTip(
            _("Scale the selected object(s)\n"
            "using the Scale Factor X for both axis."))
        self.scale_link_cb.setFixedWidth(50)

        self.scale_zero_ref_cb = FCCheckBox()
        self.scale_zero_ref_cb.set_value(True)
        self.scale_zero_ref_cb.setText(_("Scale Reference"))
        self.scale_zero_ref_cb.setToolTip(
            _("Scale the selected object(s)\n"
            "using the origin reference when checked,\n"
            "and the center of the biggest bounding box\n"
            "of the selected objects when unchecked."))

        form2_child_1.addWidget(self.scalex_entry)
        form2_child_1.addWidget(self.scalex_button)

        form2_child_2.addWidget(self.scaley_entry)
        form2_child_2.addWidget(self.scaley_button)

        form2_layout.addRow(self.scalex_label, form2_child_1)
        form2_layout.addRow(self.scaley_label, form2_child_2)
        form2_layout.addRow(self.scale_link_cb, self.scale_zero_ref_cb)
        self.ois_scale = OptionalInputSection(self.scale_link_cb, [self.scaley_entry, self.scaley_button], logic=False)

        self.transform_lay.addWidget(self.empty_label3)

        ## Offset Title
        offset_title_label = QtWidgets.QLabel("<font size=3><b>%s</b></font>" % self.offsetName)
        self.transform_lay.addWidget(offset_title_label)

        ## Form Layout
        form3_layout = QtWidgets.QFormLayout()
        self.transform_lay.addLayout(form3_layout)
        form3_child_1 = QtWidgets.QHBoxLayout()
        form3_child_2 = QtWidgets.QHBoxLayout()

        self.offx_label = QtWidgets.QLabel(_("Value X:"))
        self.offx_label.setToolTip(
            _("Value for Offset action on X axis.")
        )
        self.offx_label.setFixedWidth(50)
        self.offx_entry = FCEntry()
        self.offx_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.offx_entry.setFixedWidth(60)

        self.offx_button = FCButton()
        self.offx_button.set_value(_("Offset X"))
        self.offx_button.setToolTip(
            _("Offset the selected object(s).\n"
            "The point of reference is the middle of\n"
            "the bounding box for all selected objects.\n"))
        self.offx_button.setFixedWidth(60)

        self.offy_label = QtWidgets.QLabel(_("Value Y:"))
        self.offy_label.setToolTip(
            _("Value for Offset action on Y axis.")
        )
        self.offy_label.setFixedWidth(50)
        self.offy_entry = FCEntry()
        self.offy_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.offy_entry.setFixedWidth(60)

        self.offy_button = FCButton()
        self.offy_button.set_value(_("Offset Y"))
        self.offy_button.setToolTip(
            _("Offset the selected object(s).\n"
            "The point of reference is the middle of\n"
            "the bounding box for all selected objects.\n"))
        self.offy_button.setFixedWidth(60)

        form3_child_1.addWidget(self.offx_entry)
        form3_child_1.addWidget(self.offx_button)

        form3_child_2.addWidget(self.offy_entry)
        form3_child_2.addWidget(self.offy_button)

        form3_layout.addRow(self.offx_label, form3_child_1)
        form3_layout.addRow(self.offy_label, form3_child_2)

        self.transform_lay.addWidget(self.empty_label4)

        ## Flip Title
        flip_title_label = QtWidgets.QLabel("<font size=3><b>%s</b></font>" % self.flipName)
        self.transform_lay.addWidget(flip_title_label)

        ## Form Layout
        form4_layout = QtWidgets.QFormLayout()
        form4_child_hlay = QtWidgets.QHBoxLayout()
        self.transform_lay.addLayout(form4_child_hlay)
        self.transform_lay.addLayout(form4_layout)
        form4_child_1 = QtWidgets.QHBoxLayout()

        self.flipx_button = FCButton()
        self.flipx_button.set_value(_("Flip on X"))
        self.flipx_button.setToolTip(
            _("Flip the selected object(s) over the X axis.\n"
            "Does not create a new object.\n ")
        )
        self.flipx_button.setFixedWidth(60)

        self.flipy_button = FCButton()
        self.flipy_button.set_value(_("Flip on Y"))
        self.flipy_button.setToolTip(
            _("Flip the selected object(s) over the X axis.\n"
            "Does not create a new object.\n ")
        )
        self.flipy_button.setFixedWidth(60)

        self.flip_ref_cb = FCCheckBox()
        self.flip_ref_cb.set_value(True)
        self.flip_ref_cb.setText(_("Ref Pt"))
        self.flip_ref_cb.setToolTip(
            _("Flip the selected object(s)\n"
            "around the point in Point Entry Field.\n"
            "\n"
            "The point coordinates can be captured by\n"
            "left click on canvas together with pressing\n"
            "SHIFT key. \n"
            "Then click Add button to insert coordinates.\n"
            "Or enter the coords in format (x, y) in the\n"
            "Point Entry field and click Flip on X(Y)"))
        self.flip_ref_cb.setFixedWidth(50)

        self.flip_ref_label = QtWidgets.QLabel(_("Point:"))
        self.flip_ref_label.setToolTip(
            _("Coordinates in format (x, y) used as reference for mirroring.\n"
            "The 'x' in (x, y) will be used when using Flip on X and\n"
            "the 'y' in (x, y) will be used when using Flip on Y and")
        )
        self.flip_ref_label.setFixedWidth(50)
        self.flip_ref_entry = EvalEntry2("(0, 0)")
        self.flip_ref_entry.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.flip_ref_entry.setFixedWidth(60)

        self.flip_ref_button = FCButton()
        self.flip_ref_button.set_value(_("Add"))
        self.flip_ref_button.setToolTip(
            _("The point coordinates can be captured by\n"
            "left click on canvas together with pressing\n"
            "SHIFT key. Then click Add button to insert."))
        self.flip_ref_button.setFixedWidth(60)

        form4_child_hlay.addStretch()
        form4_child_hlay.addWidget(self.flipx_button)
        form4_child_hlay.addWidget(self.flipy_button)

        form4_child_1.addWidget(self.flip_ref_entry)
        form4_child_1.addWidget(self.flip_ref_button)

        form4_layout.addRow(self.flip_ref_cb)
        form4_layout.addRow(self.flip_ref_label, form4_child_1)
        self.ois_flip = OptionalInputSection(self.flip_ref_cb,
                                              [self.flip_ref_entry, self.flip_ref_button], logic=True)

        self.transform_lay.addStretch()

        ## Signals
        self.rotate_button.clicked.connect(self.on_rotate)
        self.skewx_button.clicked.connect(self.on_skewx)
        self.skewy_button.clicked.connect(self.on_skewy)
        self.scalex_button.clicked.connect(self.on_scalex)
        self.scaley_button.clicked.connect(self.on_scaley)
        self.offx_button.clicked.connect(self.on_offx)
        self.offy_button.clicked.connect(self.on_offy)
        self.flipx_button.clicked.connect(self.on_flipx)
        self.flipy_button.clicked.connect(self.on_flipy)
        self.flip_ref_button.clicked.connect(self.on_flip_add_coords)

        self.rotate_entry.returnPressed.connect(self.on_rotate)
        self.skewx_entry.returnPressed.connect(self.on_skewx)
        self.skewy_entry.returnPressed.connect(self.on_skewy)
        self.scalex_entry.returnPressed.connect(self.on_scalex)
        self.scaley_entry.returnPressed.connect(self.on_scaley)
        self.offx_entry.returnPressed.connect(self.on_offx)
        self.offy_entry.returnPressed.connect(self.on_offy)

    def run(self, toggle=True):
        self.app.report_usage("ToolTransform()")

        FlatCAMTool.run(self, toggle=toggle)
        self.set_tool_ui()

        self.app.ui.notebook.setTabText(2, _("Transform Tool"))

    def install(self, icon=None, separator=None, **kwargs):
        FlatCAMTool.install(self, icon, separator, shortcut='ALT+R', **kwargs)

    def set_tool_ui(self):
        ## Initialize form
        if self.app.defaults["tools_transform_rotate"]:
            self.rotate_entry.set_value(self.app.defaults["tools_transform_rotate"])
        else:
            self.rotate_entry.set_value(0.0)

        if self.app.defaults["tools_transform_skew_x"]:
            self.skewx_entry.set_value(self.app.defaults["tools_transform_skew_x"])
        else:
            self.skewx_entry.set_value(0.0)

        if self.app.defaults["tools_transform_skew_y"]:
            self.skewy_entry.set_value(self.app.defaults["tools_transform_skew_y"])
        else:
            self.skewy_entry.set_value(0.0)

        if self.app.defaults["tools_transform_scale_x"]:
            self.scalex_entry.set_value(self.app.defaults["tools_transform_scale_x"])
        else:
            self.scalex_entry.set_value(1.0)

        if self.app.defaults["tools_transform_scale_y"]:
            self.scaley_entry.set_value(self.app.defaults["tools_transform_scale_y"])
        else:
            self.scaley_entry.set_value(1.0)

        if self.app.defaults["tools_transform_scale_link"]:
            self.scale_link_cb.set_value(self.app.defaults["tools_transform_scale_link"])
        else:
            self.scale_link_cb.set_value(True)

        if self.app.defaults["tools_transform_scale_reference"]:
            self.scale_zero_ref_cb.set_value(self.app.defaults["tools_transform_scale_reference"])
        else:
            self.scale_zero_ref_cb.set_value(True)

        if self.app.defaults["tools_transform_offset_x"]:
            self.offx_entry.set_value(self.app.defaults["tools_transform_offset_x"])
        else:
            self.offx_entry.set_value(0.0)

        if self.app.defaults["tools_transform_offset_y"]:
            self.offy_entry.set_value(self.app.defaults["tools_transform_offset_y"])
        else:
            self.offy_entry.set_value(0.0)

        if self.app.defaults["tools_transform_mirror_reference"]:
            self.flip_ref_cb.set_value(self.app.defaults["tools_transform_mirror_reference"])
        else:
            self.flip_ref_cb.set_value(False)

        if self.app.defaults["tools_transform_mirror_point"]:
            self.flip_ref_entry.set_value(self.app.defaults["tools_transform_mirror_point"])
        else:
            self.flip_ref_entry.set_value((0,0))

    def on_rotate(self):
        try:
            value = float(self.rotate_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                value = float(self.rotate_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Rotate, "
                                     "use a number."))
                return
        self.app.worker_task.emit({'fcn': self.on_rotate_action,
                                       'params': [value]})
        # self.on_rotate_action(value)
        return

    def on_flipx(self):
        # self.on_flip("Y")
        axis = 'Y'
        self.app.worker_task.emit({'fcn': self.on_flip,
                                   'params': [axis]})
        return

    def on_flipy(self):
        # self.on_flip("X")
        axis = 'X'
        self.app.worker_task.emit({'fcn': self.on_flip,
                                   'params': [axis]})
        return

    def on_flip_add_coords(self):
        val = self.app.clipboard.text()
        self.flip_ref_entry.set_value(val)

    def on_skewx(self):
        try:
            value = float(self.skewx_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                value = float(self.skewx_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Skew X, "
                                     "use a number."))
                return

        # self.on_skew("X", value)
        axis = 'X'
        self.app.worker_task.emit({'fcn': self.on_skew,
                                   'params': [axis, value]})
        return

    def on_skewy(self):
        try:
            value = float(self.skewy_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                value = float(self.skewy_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Skew Y, "
                                     "use a number."))
                return

        # self.on_skew("Y", value)
        axis = 'Y'
        self.app.worker_task.emit({'fcn': self.on_skew,
                                   'params': [axis, value]})
        return

    def on_scalex(self):
        try:
            xvalue = float(self.scalex_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                xvalue = float(self.scalex_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Scale X, "
                                     "use a number."))
                return

        # scaling to zero has no sense so we remove it, because scaling with 1 does nothing
        if xvalue == 0:
            xvalue = 1
        if self.scale_link_cb.get_value():
            yvalue = xvalue
        else:
            yvalue = 1

        axis = 'X'
        point = (0, 0)
        if self.scale_zero_ref_cb.get_value():
            self.app.worker_task.emit({'fcn': self.on_scale,
                                       'params': [axis, xvalue, yvalue, point]})
            # self.on_scale("X", xvalue, yvalue, point=(0,0))
        else:
            # self.on_scale("X", xvalue, yvalue)
            self.app.worker_task.emit({'fcn': self.on_scale,
                                       'params': [axis, xvalue, yvalue]})

        return

    def on_scaley(self):
        xvalue = 1
        try:
            yvalue = float(self.scaley_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                yvalue = float(self.scaley_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Scale Y, "
                                     "use a number."))
                return

        # scaling to zero has no sense so we remove it, because scaling with 1 does nothing
        if yvalue == 0:
            yvalue = 1

        axis = 'Y'
        point = (0, 0)
        if self.scale_zero_ref_cb.get_value():
            self.app.worker_task.emit({'fcn': self.on_scale,
                                       'params': [axis, xvalue, yvalue, point]})
            # self.on_scale("Y", xvalue, yvalue, point=(0,0))
        else:
            # self.on_scale("Y", xvalue, yvalue)
            self.app.worker_task.emit({'fcn': self.on_scale,
                                       'params': [axis, xvalue, yvalue]})

        return

    def on_offx(self):
        try:
            value = float(self.offx_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                value = float(self.offx_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Offset X, "
                                     "use a number."))
                return

        # self.on_offset("X", value)
        axis = 'X'
        self.app.worker_task.emit({'fcn': self.on_offset,
                                   'params': [axis, value]})
        return

    def on_offy(self):
        try:
            value = float(self.offy_entry.get_value())
        except ValueError:
            # try to convert comma to decimal point. if it's still not working error message and return
            try:
                value = float(self.offy_entry.get_value().replace(',', '.'))
            except ValueError:
                self.app.inform.emit(_("[ERROR_NOTCL]Wrong value format entered for Offset Y, "
                                     "use a number."))
                return

        # self.on_offset("Y", value)
        axis = 'Y'
        self.app.worker_task.emit({'fcn': self.on_offset,
                                   'params': [axis, value]})
        return

    def on_rotate_action(self, num):
        obj_list = self.app.collection.get_selected()
        xminlist = []
        yminlist = []
        xmaxlist = []
        ymaxlist = []

        if not obj_list:
            self.app.inform.emit(_("[WARNING_NOTCL] No object selected. Please Select an object to rotate!"))
            return
        else:
            with self.app.proc_container.new(_("Appying Rotate")):
                try:
                    # first get a bounding box to fit all
                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            pass
                        else:
                            xmin, ymin, xmax, ymax = obj.bounds()
                            xminlist.append(xmin)
                            yminlist.append(ymin)
                            xmaxlist.append(xmax)
                            ymaxlist.append(ymax)

                    # get the minimum x,y and maximum x,y for all objects selected
                    xminimal = min(xminlist)
                    yminimal = min(yminlist)
                    xmaximal = max(xmaxlist)
                    ymaximal = max(ymaxlist)

                    self.app.progress.emit(20)

                    for sel_obj in obj_list:
                        px = 0.5 * (xminimal + xmaximal)
                        py = 0.5 * (yminimal + ymaximal)
                        if isinstance(sel_obj, FlatCAMCNCjob):
                            self.app.inform.emit(_("CNCJob objects can't be rotated."))
                        else:
                            sel_obj.rotate(-num, point=(px, py))
                            sel_obj.plot()
                            self.app.object_changed.emit(sel_obj)

                        # add information to the object that it was changed and how much
                        sel_obj.options['rotate'] = num

                    self.app.inform.emit(_('[success]Rotate done ...'))
                    self.app.progress.emit(100)

                except Exception as e:
                    self.app.inform.emit(_("[ERROR_NOTCL] Due of %s, rotation movement was not executed.") % str(e))
                    return

    def on_flip(self, axis):
        obj_list = self.app.collection.get_selected()
        xminlist = []
        yminlist = []
        xmaxlist = []
        ymaxlist = []

        if not obj_list:
            self.app.inform.emit(_("[WARNING_NOTCL] No object selected. Please Select an object to flip!"))
            return
        else:
            with self.app.proc_container.new(_("Applying Flip")):
                try:
                    # get mirroring coords from the point entry
                    if self.flip_ref_cb.isChecked():
                        px, py = eval('{}'.format(self.flip_ref_entry.text()))
                    # get mirroing coords from the center of an all-enclosing bounding box
                    else:
                        # first get a bounding box to fit all
                        for obj in obj_list:
                            if isinstance(obj, FlatCAMCNCjob):
                                pass
                            else:
                                xmin, ymin, xmax, ymax = obj.bounds()
                                xminlist.append(xmin)
                                yminlist.append(ymin)
                                xmaxlist.append(xmax)
                                ymaxlist.append(ymax)

                        # get the minimum x,y and maximum x,y for all objects selected
                        xminimal = min(xminlist)
                        yminimal = min(yminlist)
                        xmaximal = max(xmaxlist)
                        ymaximal = max(ymaxlist)

                        px = 0.5 * (xminimal + xmaximal)
                        py = 0.5 * (yminimal + ymaximal)

                    self.app.progress.emit(20)

                    # execute mirroring
                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            self.app.inform.emit(_("CNCJob objects can't be mirrored/flipped."))
                        else:
                            if axis is 'X':
                                obj.mirror('X', (px, py))
                                # add information to the object that it was changed and how much
                                # the axis is reversed because of the reference
                                if 'mirror_y' in obj.options:
                                    obj.options['mirror_y'] = not obj.options['mirror_y']
                                else:
                                    obj.options['mirror_y'] = True
                                obj.plot()
                                self.app.inform.emit(_('[success]Flip on the Y axis done ...'))
                            elif axis is 'Y':
                                obj.mirror('Y', (px, py))
                                # add information to the object that it was changed and how much
                                # the axis is reversed because of the reference
                                if 'mirror_x' in obj.options:
                                    obj.options['mirror_x'] = not obj.options['mirror_x']
                                else:
                                    obj.options['mirror_x'] = True
                                obj.plot()
                                self.app.inform.emit(_('[success]Flip on the X axis done ...'))
                            self.app.object_changed.emit(obj)
                    self.app.progress.emit(100)

                except Exception as e:
                    self.app.inform.emit(_("[ERROR_NOTCL] Due of %s, Flip action was not executed.") % str(e))
                    return

    def on_skew(self, axis, num):
        obj_list = self.app.collection.get_selected()
        xminlist = []
        yminlist = []

        if not obj_list:
            self.app.inform.emit(_("[WARNING_NOTCL] No object selected. Please Select an object to shear/skew!"))
            return
        else:
            with self.app.proc_container.new(_("Applying Skew")):
                try:
                    # first get a bounding box to fit all
                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            pass
                        else:
                            xmin, ymin, xmax, ymax = obj.bounds()
                            xminlist.append(xmin)
                            yminlist.append(ymin)

                    # get the minimum x,y and maximum x,y for all objects selected
                    xminimal = min(xminlist)
                    yminimal = min(yminlist)

                    self.app.progress.emit(20)

                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            self.app.inform.emit(_("CNCJob objects can't be skewed."))
                        else:
                            if axis is 'X':
                                obj.skew(num, 0, point=(xminimal, yminimal))
                                # add information to the object that it was changed and how much
                                obj.options['skew_x'] = num
                            elif axis is 'Y':
                                obj.skew(0, num, point=(xminimal, yminimal))
                                # add information to the object that it was changed and how much
                                obj.options['skew_y'] = num
                            obj.plot()
                            self.app.object_changed.emit(obj)
                    self.app.inform.emit(_('[success]Skew on the %s axis done ...') % str(axis))
                    self.app.progress.emit(100)

                except Exception as e:
                    self.app.inform.emit(_("[ERROR_NOTCL] Due of %s, Skew action was not executed.") % str(e))
                    return

    def on_scale(self, axis, xfactor, yfactor, point=None):
        obj_list = self.app.collection.get_selected()
        xminlist = []
        yminlist = []
        xmaxlist = []
        ymaxlist = []

        if not obj_list:
            self.app.inform.emit(_("[WARNING_NOTCL] No object selected. Please Select an object to scale!"))
            return
        else:
            with self.app.proc_container.new(_("Applying Scale")):
                try:
                    # first get a bounding box to fit all
                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            pass
                        else:
                            xmin, ymin, xmax, ymax = obj.bounds()
                            xminlist.append(xmin)
                            yminlist.append(ymin)
                            xmaxlist.append(xmax)
                            ymaxlist.append(ymax)

                    # get the minimum x,y and maximum x,y for all objects selected
                    xminimal = min(xminlist)
                    yminimal = min(yminlist)
                    xmaximal = max(xmaxlist)
                    ymaximal = max(ymaxlist)

                    self.app.progress.emit(20)

                    if point is None:
                        px = 0.5 * (xminimal + xmaximal)
                        py = 0.5 * (yminimal + ymaximal)
                    else:
                        px = 0
                        py = 0

                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            self.app.inform.emit(_("CNCJob objects can't be scaled."))
                        else:
                            obj.scale(xfactor, yfactor, point=(px, py))
                            # add information to the object that it was changed and how much
                            obj.options['scale_x'] = xfactor
                            obj.options['scale_y'] = yfactor
                            obj.plot()
                            self.app.object_changed.emit(obj)
                    self.app.inform.emit(_('[success] Scale on the %s axis done ...') % str(axis))
                    self.app.progress.emit(100)
                except Exception as e:
                    self.app.inform.emit(_("[ERROR_NOTCL] Due of %s, Scale action was not executed.") % str(e))
                    return

    def on_offset(self, axis, num):
        obj_list = self.app.collection.get_selected()
        xminlist = []
        yminlist = []

        if not obj_list:
            self.app.inform.emit(_("[WARNING_NOTCL] No object selected. Please Select an object to offset!"))
            return
        else:
            with self.app.proc_container.new(_("Applying Offset")):
                try:
                    # first get a bounding box to fit all
                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            pass
                        else:
                            xmin, ymin, xmax, ymax = obj.bounds()
                            xminlist.append(xmin)
                            yminlist.append(ymin)

                    # get the minimum x,y and maximum x,y for all objects selected
                    xminimal = min(xminlist)
                    yminimal = min(yminlist)
                    self.app.progress.emit(20)

                    for obj in obj_list:
                        if isinstance(obj, FlatCAMCNCjob):
                            self.app.inform.emit(_("CNCJob objects can't be offseted."))
                        else:
                            if axis is 'X':
                                obj.offset((num, 0))
                                # add information to the object that it was changed and how much
                                obj.options['offset_x'] = num
                            elif axis is 'Y':
                                obj.offset((0, num))
                                # add information to the object that it was changed and how much
                                obj.options['offset_y'] = num
                            obj.plot()
                            self.app.object_changed.emit(obj)
                    self.app.inform.emit(_('[success]Offset on the %s axis done ...') % str(axis))
                    self.app.progress.emit(100)

                except Exception as e:
                    self.app.inform.emit(_("[ERROR_NOTCL] Due of %s, Offset action was not executed.") % str(e))
                    return

# end of file
