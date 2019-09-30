# ##########################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# http://flatcam.org                                       #
# File Author: Marius Adrian Stanciu (c)                   #
# Date: 09/27/2019                                         #
# MIT Licence                                              #
# ##########################################################

from FlatCAMTool import FlatCAMTool
from FlatCAMObj import *
from shapely.geometry import Point
from shapely import affinity
from PyQt5 import QtCore

import collections

import gettext
import FlatCAMTranslation as fcTranslate
import builtins

fcTranslate.apply_language('strings')
if '_' not in builtins.__dict__:
    _ = gettext.gettext


class ToolOptimal(FlatCAMTool):

    toolName = _("Optimal Tool")

    def __init__(self, app):
        FlatCAMTool.__init__(self, app)

        self.units = self.app.ui.general_defaults_form.general_app_group.units_radio.get_value().upper()

        # ## Title
        title_label = QtWidgets.QLabel("%s" % self.toolName)
        title_label.setStyleSheet("""
                        QLabel
                        {
                            font-size: 16px;
                            font-weight: bold;
                        }
                        """)
        self.layout.addWidget(title_label)

        # ## Form Layout
        form_lay = QtWidgets.QFormLayout()
        self.layout.addLayout(form_lay)

        # ## Gerber Object to mirror
        self.gerber_object_combo = QtWidgets.QComboBox()
        self.gerber_object_combo.setModel(self.app.collection)
        self.gerber_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.gerber_object_combo.setCurrentIndex(1)

        self.gerber_object_label = QtWidgets.QLabel("<b>%s:</b>" % _("GERBER"))
        self.gerber_object_label.setToolTip(
            "Gerber object for which to find the minimum distance between copper features."
        )

        self.title_res_label = QtWidgets.QLabel('<b>%s</b>' % _("Minimum distance between copper features"))
        self.result_label = QtWidgets.QLabel('%s:' % _("Determined"))
        self.show_res = QtWidgets.QLabel('%s' % '')

        self.units_lbl = QtWidgets.QLabel(self.units)

        self.freq_label = QtWidgets.QLabel('%s:' % _("Frequency"))
        self.freq_label.setToolTip(_("How many times this minimum is found."))
        self.freq_res = QtWidgets.QLabel('%s' % '')

        self.precision_label = QtWidgets.QLabel('%s:' % _("Precision"))
        self.precision_label.setToolTip(_("Number of decimals kept for found distances."))

        self.precision_spinner = FCSpinner()
        self.precision_spinner.set_range(2, 10)
        self.precision_spinner.setWrapping(True)

        hlay = QtWidgets.QHBoxLayout()

        hlay.addWidget(self.show_res)
        hlay.addStretch()
        hlay.addWidget(self.units_lbl)

        form_lay.addRow(QtWidgets.QLabel(""))
        form_lay.addRow(self.gerber_object_label, self.gerber_object_combo)
        form_lay.addRow(self.precision_label, self.precision_spinner)

        form_lay.addRow(QtWidgets.QLabel(""))
        form_lay.addRow(self.title_res_label)
        form_lay.addRow(self.result_label, hlay)
        form_lay.addRow(self.freq_label, self.freq_res)

        self.calculate_button = QtWidgets.QPushButton(_("Find Distance"))
        self.calculate_button.setToolTip(
            _("Calculate the minimum distance between copper features,\n"
              "this will allow the determination of the right tool to\n"
              "use for isolation or copper clearing.")
        )
        self.calculate_button.setMinimumWidth(60)
        self.layout.addWidget(self.calculate_button)

        self.decimals = 4
        # self.dt_label = QtWidgets.QLabel("<b>%s:</b>" % _('Alignment Drill Diameter'))
        # self.dt_label.setToolTip(
        #     _("Diameter of the drill for the "
        #       "alignment holes.")
        # )
        # self.layout.addWidget(self.dt_label)
        #
        # hlay = QtWidgets.QHBoxLayout()
        # self.layout.addLayout(hlay)
        #
        # self.drill_dia = FCEntry()
        # self.dd_label = QtWidgets.QLabel('%s:' % _("Drill dia"))
        # self.dd_label.setToolTip(
        #     _("Diameter of the drill for the "
        #       "alignment holes.")
        # )
        # hlay.addWidget(self.dd_label)
        # hlay.addWidget(self.drill_dia)

        self.calculate_button.clicked.connect(self.find_minimum_distance)
        self.layout.addStretch()

        # ## Signals

    def install(self, icon=None, separator=None, **kwargs):
        FlatCAMTool.install(self, icon, separator, shortcut='ALT+O', **kwargs)

    def run(self, toggle=True):
        self.app.report_usage("ToolOptimal()")

        self.show_res.setText('')
        if toggle:
            # if the splitter is hidden, display it, else hide it but only if the current widget is the same
            if self.app.ui.splitter.sizes()[0] == 0:
                self.app.ui.splitter.setSizes([1, 1])
            else:
                try:
                    if self.app.ui.tool_scroll_area.widget().objectName() == self.toolName:
                        # if tab is populated with the tool but it does not have the focus, focus on it
                        if not self.app.ui.notebook.currentWidget() is self.app.ui.tool_tab:
                            # focus on Tool Tab
                            self.app.ui.notebook.setCurrentWidget(self.app.ui.tool_tab)
                        else:
                            self.app.ui.splitter.setSizes([0, 1])
                except AttributeError:
                    pass
        else:
            if self.app.ui.splitter.sizes()[0] == 0:
                self.app.ui.splitter.setSizes([1, 1])

        FlatCAMTool.run(self)
        self.set_tool_ui()

        self.app.ui.notebook.setTabText(2, _("Optimal Tool"))

    def set_tool_ui(self):
        self.precision_spinner.set_value(int(self.decimals))
        self.reset_fields()

    def find_minimum_distance(self):
        self.units = self.app.ui.general_defaults_form.general_app_group.units_radio.get_value().upper()
        self.decimals = int(self.precision_spinner.get_value())

        selection_index = self.gerber_object_combo.currentIndex()

        model_index = self.app.collection.index(selection_index, 0, self.gerber_object_combo.rootModelIndex())
        try:
            fcobj = model_index.internalPointer().obj
        except Exception as e:
            log.debug("ToolOptimal.find_minimum_distance() --> %s" % str(e))
            self.app.inform.emit('[WARNING_NOTCL] %s' % _("There is no Gerber object loaded ..."))
            return

        if not isinstance(fcobj, FlatCAMGerber):
            self.app.inform.emit('[ERROR_NOTCL] %s' % _("Only Gerber objects can be evaluated."))
            return

        proc = self.app.proc_container.new(_("Working..."))

        def job_thread(app_obj):
            app_obj.inform.emit(_("Optimal Tool. Started to search for the minimum distance between copper features."))
            try:
                old_disp_number = 0
                pol_nr = 0
                app_obj.proc_container.update_view_text(' %d%%' % 0)
                total_geo = list()

                for ap in list(fcobj.apertures.keys()):
                    if 'geometry' in fcobj.apertures[ap]:
                        app_obj.inform.emit(
                            '%s: %s' % (_("Optimal Tool. Parsing geometry for aperture"), str(ap)))

                        for geo_el in fcobj.apertures[ap]['geometry']:
                            if self.app.abort_flag:
                                # graceful abort requested by the user
                                raise FlatCAMApp.GracefulException

                            if 'solid' in geo_el and geo_el['solid'] is not None and geo_el['solid'].is_valid:
                                total_geo.append(geo_el['solid'])

                app_obj.inform.emit(
                    _("Optimal Tool. Creating a buffer for the object geometry."))
                total_geo = MultiPolygon(total_geo)
                total_geo = total_geo.buffer(0)

                geo_len = len(total_geo)
                geo_len = (geo_len * (geo_len - 1)) / 2

                app_obj.inform.emit(
                    '%s: %s' % (_("Optimal Tool. Finding the distances between each two elements. Iterations"),
                                str(geo_len)))

                min_list = list()
                idx = 1
                for geo in total_geo:
                    for s_geo in total_geo[idx:]:
                        if self.app.abort_flag:
                            # graceful abort requested by the user
                            raise FlatCAMApp.GracefulException

                        # minimize the number of distances by not taking into considerations those that are too small
                        dist = geo.distance(s_geo)
                        dist = float('%.*f' % (self.decimals, dist))
                        min_list.append(dist)

                        pol_nr += 1
                        disp_number = int(np.interp(pol_nr, [0, geo_len], [0, 100]))

                        if old_disp_number < disp_number <= 100:
                            app_obj.proc_container.update_view_text(' %d%%' % disp_number)
                            old_disp_number = disp_number
                    idx += 1

                app_obj.inform.emit(
                    _("Optimal Tool. Finding the minimum distance."))
                counter = collections.Counter(min_list)

                min_dist = min(min_list)
                min_dist_string = '%.*f' % (self.decimals, min_dist)
                self.show_res.setText(min_dist_string)

                freq = counter[min_dist]
                freq = '%d' % freq
                self.freq_res.setText(freq)

                app_obj.inform.emit('[success] %s' % _("Optimal Tool. Finished successfully."))
            except Exception as ee:
                proc.done()
                log.debug(str(ee))
                return
            proc.done()

        self.app.worker_task.emit({'fcn': job_thread, 'params': [self.app]})

    def reset_fields(self):
        self.gerber_object_combo.setRootModelIndex(self.app.collection.index(0, 0, QtCore.QModelIndex()))
        self.gerber_object_combo.setCurrentIndex(0)
