#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Analysis
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, blocks
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip



class record_playback(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Analysis", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Analysis")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "record_playback")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 10000
        self.samp_rate = samp_rate = 2048000
        self.sync_bw = sync_bw = 0.05
        self.squelch_threshold_db = squelch_threshold_db = -3
        self.squelch_alpha = squelch_alpha = 0.74
        self.sps = sps = samp_rate / symbol_rate
        self.fsk_deviation_hz = fsk_deviation_hz = 20e3
        self.expected_ted_gain = expected_ted_gain = 0.93
        self.bandpass_filter_width = bandpass_filter_width = 60e3

        ##################################################
        # Blocks
        ##################################################

        self._sync_bw_range = Range(0.01, 1.0, 0.01, 0.05, 200)
        self._sync_bw_win = RangeWidget(self._sync_bw_range, self.set_sync_bw, "'sync_bw'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sync_bw_win)
        self._squelch_threshold_db_range = Range(-100, 100, 1, -3, 200)
        self._squelch_threshold_db_win = RangeWidget(self._squelch_threshold_db_range, self.set_squelch_threshold_db, "'squelch_threshold_db'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._squelch_threshold_db_win)
        self._squelch_alpha_range = Range(0, 1.0, 0.0000001, 0.74, 200)
        self._squelch_alpha_win = RangeWidget(self._squelch_alpha_range, self.set_squelch_alpha, "'squelch_alpha'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._squelch_alpha_win)
        self._expected_ted_gain_range = Range(0.01, 1.0, 0.01, 0.93, 200)
        self._expected_ted_gain_win = RangeWidget(self._expected_ted_gain_range, self.set_expected_ted_gain, "'expected_ted_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._expected_ted_gain_win)
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                0.5,
                (samp_rate / 4),
                symbol_rate,
                0.98,
                512))
        self.qtgui_time_sink_x_3 = qtgui.time_sink_f(
            (1024 * 10), #size
            symbol_rate * 2, #samp_rate
            "tinst/avg", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(sps - 0.1 * sps, sps + 0.1 * sps)

        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_3.enable_tags(True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_3.enable_autoscale(False)
        self.qtgui_time_sink_x_3.enable_grid(False)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(False)
        self.qtgui_time_sink_x_3.enable_stem_plot(False)


        labels = ['inst', 'avg', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_3_win)
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_f(
            1024, #size
            symbol_rate * 2, #samp_rate
            "error", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.01)
        self.qtgui_time_sink_x_2_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0.enable_stem_plot(False)


        labels = ['error', 'error', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_0_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            symbol_rate * 2, #samp_rate
            "zzzz", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.01)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['symbols', 'error', 'bits', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, 0, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            (1024*100), #size
            samp_rate, #samp_rate
            "rootraised", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            (1024*100), #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['BinarySliced', 'QuadDemod', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            32768, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            443920000, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/60)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, '127.0.0.1', 2003, 0, 1472, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.complex_band_pass(1.0, samp_rate, fsk_deviation_hz/2 - bandpass_filter_width, fsk_deviation_hz/2 + bandpass_filter_width, bandpass_filter_width), (434100000 + 0.07e6), samp_rate)
        self.digital_symbol_sync_xx_1 = digital.symbol_sync_ff(
            digital.TED_EARLY_LATE,
            sps,
            sync_bw,
            1.0,
            expected_ted_gain,
            5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts('101010',
          0, 'zzz')
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "time" == "auto" else max( int(float(1) * samp_rate) if "time" == "time" else int(1), 1) )
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, (int(samp_rate*1.5)))
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(100)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(sps), 0.1, 4000, 1)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, (int(samp_rate*1.0)))
        self.blocks_file_meta_source_0 = blocks.file_meta_source('/tmp/capture_query.grcbin', True, False, '/tmp/capture_query.grcbin')
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc(squelch_threshold_db, squelch_alpha)
        self.analog_quadrature_demod_cf_1 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation_hz)))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'log'))
        self.connect((self.analog_quadrature_demod_cf_1, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.analog_quadrature_demod_cf_1, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.analog_quadrature_demod_cf_1, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.analog_quadrature_demod_cf_1, 0))
        self.connect((self.blocks_file_meta_source_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.digital_symbol_sync_xx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_2, 2))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_symbol_sync_xx_1, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_1, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.digital_symbol_sync_xx_1, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.digital_symbol_sync_xx_1, 1), (self.qtgui_time_sink_x_2_0, 0))
        self.connect((self.digital_symbol_sync_xx_1, 3), (self.qtgui_time_sink_x_3, 1))
        self.connect((self.digital_symbol_sync_xx_1, 2), (self.qtgui_time_sink_x_3, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_simple_squelch_cc_1, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_time_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "record_playback")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_sps(self.samp_rate / self.symbol_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.symbol_rate * 2)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.symbol_rate * 2)
        self.qtgui_time_sink_x_3.set_samp_rate(self.symbol_rate * 2)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(0.5, (self.samp_rate / 4), self.symbol_rate, 0.98, 512))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(self.samp_rate / self.symbol_rate)
        self.analog_quadrature_demod_cf_1.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation_hz)))
        self.blocks_head_0.set_length((int(self.samp_rate*1.0)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1.0, self.samp_rate, self.fsk_deviation_hz/2 - self.bandpass_filter_width, self.fsk_deviation_hz/2 + self.bandpass_filter_width, self.bandpass_filter_width))
        self.qtgui_sink_x_0.set_frequency_range(443920000, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(0.5, (self.samp_rate / 4), self.symbol_rate, 0.98, 512))

    def get_sync_bw(self):
        return self.sync_bw

    def set_sync_bw(self, sync_bw):
        self.sync_bw = sync_bw
        self.digital_symbol_sync_xx_1.set_loop_bandwidth(self.sync_bw)

    def get_squelch_threshold_db(self):
        return self.squelch_threshold_db

    def set_squelch_threshold_db(self, squelch_threshold_db):
        self.squelch_threshold_db = squelch_threshold_db
        self.analog_simple_squelch_cc_1.set_threshold(self.squelch_threshold_db)

    def get_squelch_alpha(self):
        return self.squelch_alpha

    def set_squelch_alpha(self, squelch_alpha):
        self.squelch_alpha = squelch_alpha
        self.analog_simple_squelch_cc_1.set_alpha(self.squelch_alpha)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.sps), 0.1)
        self.qtgui_time_sink_x_3.set_y_axis(self.sps - 0.1 * self.sps, self.sps + 0.1 * self.sps)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.analog_quadrature_demod_cf_1.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation_hz)))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1.0, self.samp_rate, self.fsk_deviation_hz/2 - self.bandpass_filter_width, self.fsk_deviation_hz/2 + self.bandpass_filter_width, self.bandpass_filter_width))

    def get_expected_ted_gain(self):
        return self.expected_ted_gain

    def set_expected_ted_gain(self, expected_ted_gain):
        self.expected_ted_gain = expected_ted_gain
        self.digital_symbol_sync_xx_1.set_ted_gain(self.expected_ted_gain)

    def get_bandpass_filter_width(self):
        return self.bandpass_filter_width

    def set_bandpass_filter_width(self, bandpass_filter_width):
        self.bandpass_filter_width = bandpass_filter_width
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1.0, self.samp_rate, self.fsk_deviation_hz/2 - self.bandpass_filter_width, self.fsk_deviation_hz/2 + self.bandpass_filter_width, self.bandpass_filter_width))




def main(top_block_cls=record_playback, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
