# i3-instant-layout


Automatic 'list based' layouts for the [i3](https://i3wm.org) window manager

## Animated summary
![Demo of i3-instant-layout](https://github.com/TyberiusPrime/i3-instant-layout/raw/master/docs/_static/i3-instant-layout_demo.gif "i3-instant-layout demo")


## Description

This python program drags i3 into the 'managed layouts
tiling window manager world' kicking and screaming.

What it does is apply a window layout to your current workspace,
like this one:

    -------------
    |     |  2  |
    |     |-----|
    |  1  |  3  |
    |     |-----|
    |     |  4  |
    -------------

The big advantage here  is that it needs no 'swallow' definitions whatsoever,
it's 'instant' - just add milk, eh, press the button.

## Get started

To get started, install with `pip install i3-instant-layout`, or if you prefer, [pipx](https://github.com/pipxproject/pipx)
and add this to your i3 config: 
`bindsym $mod+Escape exec "i3-instant-layout --list | rofi -dmenu -i | i3-instant-layout -` (or use the interactive menu of your choice).


## Further information

Call `i3-instant-layout --help` for full details, or 
`i3-instant-layout --desc` for the full list of supported layouts (or see below).


## Helpful tips

To get the windows in the right order for your layout of choice,
first enable the vStack or hStack layout, sort them,
and the proceed to your layout of choice.


## Available layouts

Layout: vStack

Aliases: ['1col', '1c']

One column / a vertical stack.

	---------
	|   1   |
	---------
	|   2   |
	---------
	|   3   |
	---------


--------------------------------------------------------------------------------

Layout: hStack

Aliases: ['1row', '1r']

One row / a horizontal stack

	-------------
	|   |   |   |
	| 1 | 2 | 3 |
	|   |   |   |
	-------------


--------------------------------------------------------------------------------

Layout: v2Stack

Aliases: ['2col', '2c', '2v']

Two columns of stacks
	
	-------------
	|  1  |  4  |
	-------------
	|  2  |  5  |
	-------------
	|  3  |  6  |
	-------------


--------------------------------------------------------------------------------

Layout: h2Stack

Aliases: ['2row', '2r', '2h']

Two rows of stacks
	
	-------------------
	|  1  |  2  |  3  |
	-------------------
	|  4  |  5  |  6  |
	-------------------


--------------------------------------------------------------------------------

Layout: v3Stack

Aliases: ['3col', '3c', '3v']

Three columns of stacks

	-------------------
	|  1  |  3  |  5  |
	-------------------
	|  2  |  4  |  6  |
	-------------------


--------------------------------------------------------------------------------

Layout: h3Stack

Aliases: ['3row', '3r', '3h']

Three rows of stacks

	-------------------
	|  1  |  2  |  3  |
	-------------------
	|  4  |  5  |  6  |
	-------------------
	|  7  |  8  |  9  |
	-------------------


--------------------------------------------------------------------------------

Layout: max

Aliases: ['maxTabbed']

One large container, in tabbed mode.

	---------------
	|             |
	|   1,2,3,4,  |
	|             |
	---------------


--------------------------------------------------------------------------------

Layout: mainLeft

Aliases: ['ml', 'mv', 'MonadTall']

One large window to the left at 50%,
all others stacked to the right vertically.

	-------------
	|     |  2  |
	|     |-----|
	|  1  |  3  |
	|     |-----|
	|     |  4  |
	-------------


--------------------------------------------------------------------------------

Layout: mainRight

Aliases: ['mr', 'vm', 'MonadTallFlip']

One large window to the right at 50%,
all others stacked to the right vertically.

	-------------
	|  2  |     |
	|-----|     |
	|  3  |  1  |
	|-----|     |
	|  4  |     |
	-------------


--------------------------------------------------------------------------------

Layout: MainMainVStack

Aliases: ['mmv']

Two large windows to the left at 30%,
all others stacked to the right vertically.

	-------------------
	|     |     |  3  |
	|     |     |-----|
	|  1  |  2  |  4  |
	|     |     |-----|
	|     |     |  5  |
	-------------------


--------------------------------------------------------------------------------

Layout: MainVStackMain

Aliases: ['mvm']

Two large windows at 30% to the left and right,
a vstack in the center

	-------------------
	|     |  3  |     |
	|     |-----|     |
	|  1  |  4  |  2  |
	|     |-----|     |
	|     |  5  |     |
	-------------------


--------------------------------------------------------------------------------

Layout: matrix

Aliases: []

Place windows in a n * n matrix.

The matrix will place swallow-markers
if you have less than n*n windows.

N is math.ceil(math.sqrt(window_count))


--------------------------------------------------------------------------------

Layout: VerticalTileTop

Aliases: ['vtt']

Large master area (66%) on top,
horizontal stacking below


--------------------------------------------------------------------------------

Layout: VerticalTileBottom

Aliases: ['vtb']

Large master area (66%) on bottom,
horizontal stacking above


--------------------------------------------------------------------------------

Layout: NestedRight

Aliases: ['nr']

Nested layout, starting with a full left half.


	-------------------------
	|           |           |
	|           |     2     |
	|           |           |
	|     1     |-----------|
	|           |     |  4  |
	|           |  3  |-----|
	|           |     |5 | 6|
	-------------------------


--------------------------------------------------------------------------------

Layout: SmartNestedRight

Aliases: ['snr']

Nested layout, starting with a full left half,
but never going below 1/16th of the size.

	2 windows
	-------------------------
	|           |           |
	|           |           |
	|           |           |
	|     1     |     2     |
	|           |           |
	|           |           |
	|           |           |
	-------------------------

	5 windows
	-------------------------
	|           |           |
	|           |     2     |
	|           |           |
	|     1     |-----------|
	|           |     |  4  |
	|           |  3  |-----|
	|           |     |  5  |
	-------------------------

	6 windows
	-------------------------
	|           |           |
	|           |     2     |
	|           |           |
	|     1     |-----------|
	|           |  3  |  4  |
	|           |-----|-----|
	|           |  5  |  6  |
	-------------------------

	7 windows
	-------------------------
	|           |     |     |
	|           |  2  |  3  |
	|           |     |     |
	|     1     |-----------|
	|           |  4  |  5  |
	|           |-----|-----|
	|           |  6  |  7  |
	-------------------------


	15 windows
	-------------------------
	|     |  2  |  4  |  6  |
	|  1  |-----|-----|-----|
	|     |  3  |  5  |  7  |
	|-----------|-----------|
	|  8  |  A  |  C  |  E  |
	|-----|-----|-----|-----|
	|  9  |  B  |  D  |  F  |
	-------------------------

Falls back to matrix layout above 16 windows.


--------------------------------------------------------------------------------

