import json
import os

import Imath
import matplotlib.pyplot as plt
import numpy as np
import OpenEXR

depth_data_dir = r"...\depth_z.exr"
clib_dir = r"...\calib.json"


def load_depth_exr(path):
    f = OpenEXR.InputFile(path)
    dw = f.header()["dataWindow"]
    w = dw.max.x - dw.min.x + 1
    h = dw.max.y - dw.min.y + 1
    ch = "R" if "R" in f.header()["channels"] else next(iter(f.header()["channels"]))
    raw = f.channel(ch, Imath.PixelType(Imath.PixelType.FLOAT))
    return np.frombuffer(raw, dtype=np.float32).reshape(h, w)


def main():
    '''visualize the depth data'''
    with open(clib_dir, encoding="utf-8") as f:
        calib = json.load(f)
    unit = calib.get("unit", "?")
    res = tuple(calib["camera"]["resolution"])  # [w, h]

    z = load_depth_exr(depth_data_dir)
    assert z.shape == (res[1], res[0]), f"depth {z.shape} != calib {res[1]}x{res[0]}"

    lo, hi = np.nanpercentile(z, [2, 98])
    print("z clim", lo, hi, "valid", np.isfinite(z).sum(), f"unit={unit}")

    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(z, cmap="turbo", vmin=lo, vmax=hi)
    ax.set_title(f"Z = depth (camera) [{unit}]")
    ax.axis("off")
    plt.colorbar(im, ax=ax)
    plt.tight_layout()

    out = os.path.join(os.path.dirname(depth_data_dir), "depth_vis.png")
    plt.savefig(out, dpi=120)
    print("saved", out)
    plt.show()


if __name__ == "__main__":
    main()
