import math

layouts = []


def register_layout(cls):
    layouts.append(cls)
    return cls


def node(percent, layout, swallows, children):
    result = {
        "border": "normal",
        # "current_border_width": 2,
        "floating": "auto_off",
        # "name": "fish  <</home/finkernagel>>",
        "percent": percent,
        "type": "con",
        "layout": layout,
    }
    if swallows:
        result["swallows"] = ([{"class": "."}],)
    if children:
        result["nodes"] = children
    return result


def get_stack(window_count, split):
    return get_stack_unequal([1.0 / window_count] * window_count, split)


def get_stack_unequal(percentages, split):
    elements = []
    for p in percentages:
        elements.append(node(p, split, True, False))
    return [{"layout": split, "type": "con", "nodes": elements}]


@register_layout
class Layout_vStack:

    name = "vStack"
    aliases = ["1col", "1c"]
    description = """\
            One column / a vertical stack.

    ---------
    |   1   |
    ---------
    |   2   |
    ---------
    |   3   |
    ---------
    """

    def get_json(self, window_count):
        return get_stack(window_count, "splitv")


@register_layout
class Layout_hStack:

    name = "hStack"
    aliases = ["1row", "1r"]
    description = """\
            One row / a horizontal stack

    -------------
    |   |   |   |
    | 1 | 2 | 3 |
    |   |   |   |
    -------------
    """

    def get_json(self, window_count):
        return get_stack(window_count, "splith")


@register_layout
class Layout_v2Stack:

    name = "v2Stack"
    aliases = ["2col", "2c", "2v"]
    description = """\
            Two columns of stacks
    -------------
    |  1  |  4  |
    -------------
    |  2  |  5  |
    -------------
    |  3  |  6  |
    -------------
    """

    def get_json(self, window_count):
        s = int(math.ceil(window_count / 2))
        left = get_stack(s, "splitv")
        right = get_stack(s if window_count % 2 == 0 else s - 1, "splitv")
        return [{"layout": "splith", "type": "con", "nodes": [left, right]}]


@register_layout
class Layout_h2Stack:

    name = "h2Stack"
    aliases = ["2row", "2r", "2h"]
    description = """\
            Two rows of stacks
    -------------------
    |  1  |  2  |  3  |
    -------------------
    |  4  |  5  |  6  |
    -------------------
    """

    def get_json(self, window_count):
        s = int(math.ceil(window_count / 2))
        left = get_stack(s, "splith")
        right = get_stack(s if window_count % 2 == 0 else s - 1, "splith")
        return [{"layout": "splitv", "type": "con", "nodes": [left, right]}]


@register_layout
class Layout_v3Stack:

    name = "v3Stack"
    aliases = ["3col", "3c", "3v"]
    description = """\
            Three columns of stacks
    -------------------
    |  1  |  3  |  5  |
    -------------------
    |  2  |  4  |  6  |
    -------------------
    """

    def get_json(self, window_count):
        s = window_count // 3
        a = get_stack(s + window_count % 3, "splitv")
        b = get_stack(s, "splitv")
        c = get_stack(s, "splitv")
        return [{"layout": "splith", "type": "con", "nodes": [a, b, c]}]


@register_layout
class Layout_h3Stack:

    name = "h3Stack"
    aliases = ["3row", "3r", "3h"]
    description = """\
            Three rows of stacks
    -------------------
    |  1  |  2  |  3  |
    -------------------
    |  4  |  5  |  6  |
    -------------------
    |  7  |  8  |  9  |
    -------------------
    """

    def get_json(self, window_count):
        s = window_count // 3
        a = get_stack(s + window_count % 3, "splith")
        b = get_stack(s, "splith")
        c = get_stack(s, "splith")
        return [{"layout": "splitv", "type": "con", "nodes": [a, b, c]}]


@register_layout
class Layout_Max:

    name = "max"
    aliases = ["maxTabbed"]
    description = """\
            One large container,
        in tabbed mode.

       ---------------
       |             |
       |   1,2,3,4,  |
       |             |
       ---------------
    """

    def get_json(self, window_count):
        return get_stack(window_count, "tabbed")


@register_layout
class Layout_MainLeft:

    name = "mainLeft"
    aliases = ["ml", "mv", "MonadTall"]
    description = """\
            One large window to the left at 50%,
            all others stacked to the right vertically.

            -------------
            |     |  2  |
            |     |-----|
            |  1  |  3  |
            |     |-----|
            |     |  4  |
            -------------
            """

    def get_json(self, window_count):
        return node(
            1,
            "splith",
            False,
            [node(0.5, "splitv", True, []), get_stack(window_count - 1, "splitv")],
        )


@register_layout
class Layout_MainRight:

    name = "mainRight"
    aliases = ["mr", "vm", "MonadTallFlip"]
    description = """\
            One large window to the right at 50%,
            all others stacked to the right vertically.

            -------------
            |  2  |     |
            |-----|     |
            |  3  |  1  |
            |-----|     |
            |  4  |     |
            -------------
            """

    def get_json(self, window_count):
        return (
            node(
                1,
                "splith",
                False,
                [get_stack(window_count - 1, "splitv"), node(0.5, "splitv", True, [])],
            ),
            list(range(1, window_count)) + [0],
        )


@register_layout
class Layout_MainMainVStack:

    name = "MainMainVStack"
    aliases = ["mmv"]
    description = """\
            Two large windows to the left at 30%,
            all others stacked to the right vertically.

            -------------------
            |     |     |  3  |
            |     |     |-----|
            |  1  |  2  |  4  |
            |     |     |-----|
            |     |     |  5  |
            -------------------
            """

    def get_json(self, window_count):
        return node(
            1,
            "splith",
            False,
            [
                node(1 / 3, "splitv", True, []),
                node(1 / 3, "splitv", True, []),
                get_stack(window_count - 2, "splitv"),
            ],
        )


@register_layout
class Layout_MainVStackMain:

    name = "MainVStackMain"
    aliases = ["mvm"]
    description = """\
            Two large windows at 30% to the left and right,
            a vstack in the center

            -------------------
            |     |  3  |     |
            |     |-----|     |
            |  1  |  4  |  2  |
            |     |-----|     |
            |     |  5  |     |
            -------------------
            """

    def get_json(self, window_count):
        return (
            node(
                1,
                "splith",
                False,
                [
                    node(1 / 3, "splitv", True, []),
                    get_stack(window_count - 2, "splitv"),
                    node(1 / 3, "splitv", True, []),
                ],
            ),
            [0] + list(range(2, window_count)) + [1],
        )


@register_layout
class Layout_Matrix:

    name = "matrix"
    aliases = []
    description = """\
            Place windows in a n * n matrix.

            The matrix will place swallow-markers
            if you have less than n*n windows.

            N is math.ceil(math.sqrt(window_count))
        """

    def get_json(self, window_count):
        n = int(math.ceil(math.sqrt(window_count)))
        stacks = [get_stack(n, "splith") for stack in range(n)]
        return node(1, "splitv", False, stacks)


@register_layout
class Layout_VerticalTileTop:

    name = "VerticalTileTop"
    aliases = ["vtt"]
    description = """\
            Large master area (66%) on top,
            horizontal stacking below
            """

    def get_json(self, window_count):
        return node(
            1,
            "splitv",
            False,
            [
                node(0.66, "splitv", True, []),
                node(
                    0.33,
                    "splitv",
                    False,
                    get_stack_unequal(
                        [0.33 / (window_count - 1)] * (window_count - 1), "splitv",
                    ),
                ),
            ],
        )


@register_layout
class Layout_VerticalTileBottom:

    name = "VerticalTileBottom"
    aliases = ["vtb"]
    description = """\
            Large master area (66%) on bottom,
            horizontal stacking above
            """

    def get_json(self, window_count):
        return (
            node(
                1,
                "splitv",
                False,
                [
                    node(
                        0.33,
                        "splitv",
                        False,
                        get_stack_unequal(
                            [0.33 / (window_count - 1)] * (window_count - 1), "splitv",
                        ),
                    ),
                    node(0.66, "splitv", True, []),
                ],
            ),
            list(range(1, window_count)) + [0],
        )


@register_layout
class Nested:
    name = "NestedRight"
    aliases = ["nr"]

    description = """\
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
            """

    def get_json(self, window_count):
        dir = "h"
        parent = node(1, "splith", False, [])
        root = parent
        parent["nodes"] = []
        for ii in range(window_count):
            parent["nodes"].append(get_stack_unequal([0.5], "split" + dir))
            n = node(1, "splith", False, [])
            if dir == "h":
                dir = "v"
            else:
                dir = "h"

            n["layout"] = "split" + dir
            n["nodes"] = []
            if ii < window_count - 1:
                parent["nodes"].append(n)
                parent = n
        return root


@register_layout
class Smart:
    name = "SmartNestedRight"
    aliases = ["snr"]

    description = """\
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
            """

    def get_json(self, window_count):
        def nest_1():
            return node(1, "splith", True, [])

        def nest_2():
            return get_stack(2, "splith")

        def nest_3():
            return node(
                1,
                "splith",
                False,
                [node(0.5, "splitv", True, []), get_stack(2, "splitv")],
            )

        def nest_4():
            return node(
                1, "splith", False, [get_stack(2, "splitv"), get_stack(2, "splitv")],
            )

        if window_count == 1:
            return nest_1()
        elif window_count == 2:
            return nest_2()
        elif window_count == 3:
            return nest_3()
        elif window_count == 4:
            return nest_4()
        elif window_count == 5:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", True, [],),
                    node(
                        0.5, "splitv", False, [node(0.5, "split", True, []), nest_3()]
                    ),
                ],
            )
        elif window_count == 6:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", True, [],),
                    node(
                        0.5, "splitv", False, [node(0.5, "split", True, []), nest_4()]
                    ),
                ],
            )
        elif window_count == 7:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", True, [],),
                    node(0.5, "splitv", False, [nest_2(), nest_4()]),
                ],
            )
        elif window_count == 8:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", True, [],),
                    node(0.5, "splitv", False, [nest_3(), nest_4()]),
                ],
            )
        elif window_count == 9:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", True, [],),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 10:
            return node(
                1,
                "splith",
                False,
                [
                    node(
                        0.5,
                        "splitv",
                        False,
                        [node(0.5, "splitv", True, []), node(0.5, "splitv", True, [])],
                    ),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 11:
            return node(
                1,
                "splith",
                False,
                [
                    node(
                        0.5, "splitv", False, [node(0.5, "splitv", True, []), nest_2()],
                    ),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 12:
            return node(
                1,
                "splith",
                False,
                [
                    node(
                        0.5, "splitv", False, [node(0.5, "splitv", True, []), nest_3()],
                    ),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 13:
            return node(
                1,
                "splith",
                False,
                [
                    node(
                        0.5, "splitv", False, [node(0.5, "splitv", True, []), nest_4()],
                    ),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 14:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", False, [nest_2(), nest_4()],),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 15:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", False, [nest_3(), nest_4()],),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        elif window_count == 16:
            return node(
                1,
                "splith",
                False,
                [
                    node(0.5, "splitv", False, [nest_4(), nest_4()],),
                    node(0.5, "splitv", False, [nest_4(), nest_4()]),
                ],
            )
        else:
            return Layout_Matrix().get_json(window_count)
