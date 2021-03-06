### MFP -- music for programmers 

MFP is an environment for visually composing computer programs, with
an emphasis on music and real-time audio synthesis and analysis.  It's
very much inspired by Miller Puckette's Pure Data (pd) and MAX/MSP,
with a bit of LabView and TouchOSC for good measure.  

MFP is in its early development phases.  Large pieces of core functionality
are not implemented yet, including:  undo, JACK MIDI, i18n, audio file
reading, etc etc etc.

What IS there is the basic program window and patch editor, enough
message and DSP processors to build some useful patches, a model for how
a mostly-keyboard-controlled GUI app will work, and the infrastructure
of the 3 separate processes (main, GUI, and DSP) that work together to
make MFP happen. 

### BUILDING

See README.build 

### USAGE

Try:  

    mfp -h for a command line arguments summary.  
    mfp --help-builtins lists the name and tooltip of every builtin object. 

**Hello, world:** Follow these steps to create a helloworld patch
using just the keyboard.  You do need a pointer to activate it. 

You type | What happens
---------|----------------
a | Autoplace mode.  A + appears where the next object will go
m | Create message (literal data)
"hello world" RET| Put the string "hello, world" in the message 
c | Connect mode (will connect selected object to something)
a | Autoplace mode again
p | Create a processor
print RET | Make it a [print] processor
RET | Make the connection
ESC | Enter Operate major mode 

Now click on the message box to send the "hello, world" string.  

Below the patch editing area, in the "Log" tab, you will see the message 
appear.

At any time, the "Keybindings" tab to the left of the patch editing area
will show you all the active key bindings.  Bindings nearer the top are 
chosen first, so if there are 2 listings for RET for instance the top one will
be used.

If you hover the mouse over any object, a tooltip with some
documentation will appear at the top of the canvas area.  Hold down
SHIFT to expand the tooltip to show current information about the
object, including assigned MIDI and OSC controllers. 

**Tutorial:**  The file "tutorial.mfp" is a basic intro to
getting around the program.  

    $ mfp doc/tutorial.mfp 

**Demo patches:** There are a few demo patches in doc/ which are really all the
documentation there is right now. 

If your $PWD is in the doc/ directory, just run the demo patch by putting
the file name on the command line, i.e. 

    $ mfp hello_world.mfp

To run it from elsewhere, use the "-p" option to add the doc directory
to your MFP searchpath.  For example, from the top-level src
directory, 

    $ mfp -p doc hello_world.mfp


hello_world.mfp:  The classic 

biquad_designer.mfp:  Not complete!  But at least partly working.  Click
the "calculate" button to compute biquad coefficients and audition them
with a noise input source (I run this into JAAA to check my calculations).
PGDN to shift to the Graphs layer with pole/zero and analytical frequency
response.  You need to add doc/ to the patch search path for this to load 
(it uses the "quadratic.mfp" patch).  From the directory holding this 
README: 

    $ mfp -p doc doc/biquad_designer.mfp

oscope.mfp: Simple demo of the signal<-->control level bridge provided by
numpy and the buffer~ object.  A very basic oscilloscope. 

looper.mfp: A simple overdubbing loop sampler inspired by the Akai
Headrush, also built around a [buffer~].  

monomix.mfp: A demonstration of how to make a vanilla user patch with
variable numbers of inputs, determined by an init argument.  For
example, [monomix 4] makes a mixer with 4 signal inputs, 4 sliders,
and 1 signal output.  This makes use of the @clonescope method and the
concept of hygienic layer copying. 


### SAVING FILES

There's no UI for saving yet, but there is a key mapping.
C-s (control-s) will prompt for a file to save in.  There's no checking for
overwrite, and the file is saved in the process working directory. 

### REPORTING PROBLEMS

I'm using the GitHub hosted issue tracker.  It seems to be pretty
workable.  

Enjoy! 

Bill Gribble <grib@billgribble.com>
