"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


"""
https://www.gnuradio.org/doc/doxygen-3.7/page_python_blocks.html
numpy.int8
numpy.int16
numpy.int32
numpy.float32
numpy.float64
"""

class blkz(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, storage_file="/tmp/ramdisk/our_bits.bin"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='WriteBitsToFile',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[]
        )
        if storage_file is None:
            storage_file = "/tmp/ramdisk/our_bits.bin"
        self.storage_file = storage_file

    def work(self, input_items, output_items):
        # print(type(input_items))
        # print(input_items)
        self.f.write(input_items[0].tobytes())
        return 0



    def start(self):
        self.f = open(self.storage_file, "wb")

    def stop(self):
        self.f.close()
        self.f = None
