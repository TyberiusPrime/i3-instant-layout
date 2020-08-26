import asyncio
import datetime
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from . import layouts


counter_file = Path("~/.local/share/i3-instant-layout/counter.json").expanduser()
counter_file.parent.mkdir(exist_ok=True, parents=True)


def append_layout(layout_dict, window_count):
    """Apply a layout from this layout class"""
    tf = tempfile.NamedTemporaryFile(suffix=".json")
    tf.write(json.dumps(layout_dict, indent=4).encode("utf-8"))
    tf.flush()
    cmd = ["i3-msg", "append_layout", str(Path(tf.name).absolute())]
    subprocess.check_call(cmd, stdout=subprocess.PIPE)
    tf.close()


def get_window_ids():
    """use xprop to list windows on current screen.

    Couldn't find out how to get the right ids from i3ipc.
    id is con_id, but we need x11 id

    Sorry, this probably means this won't work on wayland & sway.
    """

    desktop = subprocess.check_output(
        ["xprop", "-notype", "-root", "_NET_CURRENT_DESKTOP"]
    ).decode("utf-8", errors="replace")
    desktop = desktop[desktop.rfind("=") + 2 :].strip()
    res = subprocess.check_output(
        [
            "xdotool",
            "search",
            "--all",
            "--onlyvisible",
            "--desktop",
            desktop,
            "--class",
            "",
        ]
    ).decode("utf-8", errors="replace")
    return res.strip().split("\n")


def get_active_window():
    return (
        subprocess.check_output(["xdotool", "getactivewindow"]).decode("utf-8").strip()
    )


def focus_window(id):
    return subprocess.check_call(
        ["i3-msg", f'[id="{id}"]', "focus"], stdout=subprocess.PIPE
    )
    # return subprocess.check_call(['xdotool','windowraise', id])


def apply_layout(layout, dry_run=False):
    """Actually turn this workspace into this layout"""
    active = get_active_window()
    windows = get_window_ids()
    window_count = len(windows)
    # we unmap and map all at once for speed.
    unmap_cmd = [
        "xdotool",
    ]
    map_cmd = [
        "xdotool",
    ]
    t = layout.get_json(window_count)
    if isinstance(t, tuple):
        layout_dict, remap_order = t
        if set(range(window_count)) != set(remap_order):
            raise ValueError("Layout returned invalid remap order")
        windows = [windows[ii] for ii in remap_order]
    else:
        layout_dict = t

    if dry_run:
        print(json.dumps(layout_dict, indent=4))
    else:
        if layout_dict is not False:
            append_layout(layout_dict, window_count)
            for window_id in windows:
                unmap_cmd.append("windowunmap")
                map_cmd.append("windowmap")
                unmap_cmd.append(str(window_id))
                map_cmd.append(str(window_id))

            # force i3 to swallow these windows.
            subprocess.check_call(unmap_cmd)
            subprocess.check_call(map_cmd)
            focus_window(active)


def load_usage():
    try:
        with open(counter_file, "r") as op:
            return json.load(op)
    except (OSError, ValueError):
        return {}


def count_usage(layout_name):
    usage = load_usage()
    if layout_name not in usage:
        usage[layout_name] = (0, datetime.datetime.now().timestamp())
    usage[layout_name] = (
        usage[layout_name][0] + 1,
        datetime.datetime.now().timestamp(),
    )

    with open(counter_file, "w") as op:
        json.dump(usage, op)


def list_layouts_in_smart_order():
    """List the layouts in a 'smart' order,
    that means most common ones on top (by log10 usage),
    within one log10 unit, sorted by most-recently-used"""
    usage = load_usage()
    sort_me = []
    for layout in layouts.layouts:
        if " " in layout.name:
            raise ValueError(
                f"No spaces in layout names please. Offender: '{layout.name}'"
            )
        for alias in [layout.name] + layout.aliases:
            usage_count, last_used = usage.get(
                alias, (0, datetime.datetime.now().timestamp())
            )
            if alias == layout.name:
                desc = alias
            else:
                desc = f"{alias} ({layout.name})"
            sort_me.append(
                (-1 * math.ceil(math.log10(usage_count + 1)), -1 * last_used, desc)
            )
    sort_me.sort()
    for _, _, name in sort_me:
        print(name)


def print_help():
    print(
        """i3-instant-layout applies ready made layouts to i3 workspaces,
    based on the numerical position of the windows.

    Call with '--list' to get a list of available layouts (and their aliases).

    Call with --desc to get detailed information about every layout available.

    Call with the name of a layout to apply it to the current workspace.

    Call with '-' to read layout name from stdin.

    Call with 'name --dry-run' to inspect the generated i3 append_layout compatible json.

    To integrate into i3, add this to your i3/config.
        bindsym $mod+Escape exec "i3-instant-layout --list | rofi -dmenu -i | i3-instant-layout -"

    """
    )
    sys.exit(0)


def print_desc():
    import textwrap

    for layout_class in layouts.layouts:
        print(f"Layout: {layout_class.name}")
        print(f"Aliases: {layout_class.aliases}")
        print(textwrap.indent(textwrap.dedent(layout_class.description), "\t"))
        print("")
        print("-" * 80)
        print("")


def main():
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        print_help()
    elif sys.argv[1] == "--desc":
        print_desc()
        sys.exit(0)
    elif sys.argv[1] == "--list":
        list_layouts_in_smart_order()
        sys.exit(0)
    elif sys.argv[1] == "-":
        query = sys.stdin.readline().strip()
        print(f'query "{query}"')
        if not query.strip():  # e.g. rofi cancel
            sys.exit(0)
    else:
        query = sys.argv[1]
    if " " in query:
        query = query[: query.find(" ")]
    for layout_class in layouts.layouts:
        if query == layout_class.name or query in layout_class.aliases:
            apply_layout(layout_class(), "--dry-run" in sys.argv)
            count_usage(query)
            sys.exit(0)
    else:
        print("Could not find the requested layout")
        sys.exit(1)
