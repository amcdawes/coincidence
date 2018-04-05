# Coincidence Counter
## An interface for the coincidence counter by Eric Ayars

This software requires several additional python packages. To make it as simple as possible for anyone to use, I recommend starting with the [Anaconda python distribution](https://www.anaconda.com/download/) (free and easy to install).

I am happy to help with that process, but it is fairly well documented, and very well-maintained software.

Once anaconda is installed, you will need two additional python libraries. These can be installed via the command line:

`conda install pyserial`
`conda install bokeh`

[Bokeh](https://bokeh.pydata.org/en/latest/) is a powerful visualization package for python. It includes web-based interfaces that provide widgets like sliders, graphs, and text-based readout for display of values.

Plug the coincidence counter into a usb port. This software communicates via serial and is set up to request counts every 100 ms. Averages for A and B are displayed (with standard deviation). Also, the value of g(2) is calculated and assumes that the coincidence counter is configured for counting coincidences as follows:
```
0:1000
1:0100
2:0010
3:0001
4:1100
5:1010
6:1001
7:1110
```
In other words, counters 0-3 are singles counts for each input, and counters 4,5,6 are two-fold coincidences with the first input, and the 7th counter is a three-fold coincidence between the first three input. These can be set by sending serial commands to the coincidence unit. The full help text is listed below.

To use this interface, run the following from the command line in the repository directory:

`bokeh serve --show coinc`

This starts a bokeh web server (running locally) and opens a web browser with the interface display.

Commands for the coincidence unit, shown by sending command `h`:
```
Coincidence Detector CD48
Eric Ayars, 2018

    "If you think you understand Quantum Mechanics,
    You don't understand Quantum Mechanics."
                --Richard Feynman

Commands:
  C - Report counts on channels 0-6 and error status.
    Human-readable format.
  c - (lower case) reports channels 0-6, space-delimited, followed by error sta
    Not as human-readable, better for LabVIEW parsing.
  E - Report and clear overflow flag.
  H - Help (this message).
  Ln - Set input trigger level to n.
    0<=n<=255 which maps to 0-4.08V.
    i.e. L127 sets trigger to 2.024V.
  P - Prints all settings: channel targets, repeat time, repeat status,
    trigger level, and impedance.
    This printout is in a nice human-readable format.
  p - (lower case) reports channel settings in 4-bit (nibble) number,
        followed by repeat time, repeat status, trigger level, and impedance.
        Not as human-readable, better for LabVIEW parsing.
  rn - Sets repeat interval to n ms for reporting channel counts.
    i.e. 'R2000' -> 2-second repeat.
    minimum n = 100, maximum = 65535. If outside that range, device sets to lim.
        For count periods larger than 65s, use external control via 'C/c'.
  R - Toggles repeat state. Off by default.
  SnABCD - Set channel to desired inputs.
    n = channel number
        ABCD = 1 or 0 for each input.
    i.e. 'S31010' sets counter 3 to watch A and C, not B or D.
        Note: channels 0-6 are 24-bit (max 16,777,215), 7 is 16-bit (65,535).
  T - Turn on all LEDs for 1s.
  Vn - Set output voltage to n. Note that n must be a byte, actual voltage rang
    linearly from 0-4.08 over a range of n=0 to n=255.
  v - Return firmware version.
  Z - Set input impedance high.
  z - Set input impedance to 50 Ohms.

If a command is successful, the 'comm' light will blink in response.
```
