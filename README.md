
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

Looks like an 10 kHz bitrate. Likely manchester encoded.



The [rtl_433](https://triq.org/rtl_433/) project also looks interesting:
`nix run current#rtl_433 -- -s 2048000  -X "n=dongle,modulation=FSK_MC_ZEROBIT,s=100,l=100,reset=1000"`




https://wiki.gnuradio.org/index.php?title=Symbol_Sync

