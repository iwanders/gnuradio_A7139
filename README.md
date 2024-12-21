# Gnuradio A7139


Decoding an A7139 434 MHz FSK radio transmission with gnuradio.

Current state:
- Signal processing working
- Demodulation working
- Symbol sync / looks to be working
- We get bits, but we don't yet know where the preamble stops and where data starts.

### Bitrate calculation
Up-down preamble;

bit is from 436213.02 us to 436314.69 us

0.00010166999999999815 s per bit?

Start at 435210.93e-6, we count; 29 symbols to 438118.58e-6


```
>>> e = 438118.58e-6
>>> s = 435210.93e-6
>>> e-s
0.002907649999999984
>>> (e-s) / 29
0.00010026379310344772
```

Looks like an 10 kHz bitrate. Likely manchester encoded?

Chip supports three bit stream processess;
- CCIT-16 CRC
- (7,4) Hamming FEC
- Data whitening with XOR.

CRC is over the payload only, preamble and ID code are ignored.
FEC; over payload AND CRC. Each 4 bit nibble is encoded into 7 bits code word; 64 byte payload becomes 128 code words, each code word 7 bits.
Whitening: Is this just an XOR with a fixed value? happens after CRC and FEC.


### Random links / notes
The [rtl_433](https://triq.org/rtl_433/) project also looks interesting:
`nix run current#rtl_433 -- -s 2048000  -X "n=dongle,modulation=FSK_MC_ZEROBIT,s=100,l=100,reset=1000"`




https://wiki.gnuradio.org/index.php?title=Symbol_Sync


https://wiki.gnuradio.org/index.php?title=QPSK_Mod_and_Demod#7.6._Recovering_Timing



probably a crc in there... it would be nice if we could have a 'tags to pdu' block, that starts on the sync word / preamble, and terminates when a crc is valid?


Capture the udp stream with
```
nc -u -l -k 127.0.0.1 2003 | hexdump -C
```


### To pulseview/sigrok

Using the new python block to write data to disk (recommand a ramdisk).

Non packed bytes, then
```
sigrok-cli -I binary:numchannels=1:samplerate=204800 -i our_bits.bin  -o ourdata.sr
```

