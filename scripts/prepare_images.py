"""One-time image prep from the design mock-up (needs opencv-python + numpy).

  python scripts/prepare_images.py path/to/Straw_Hat_Developer_Portfolio_Dashboard.png

Produces assets/img/*.jpg: the cover with every baked-in label AND the round
captain avatar removed (so the art can zoom slowly behind crisp, still text),
and the other panels. You only need this again if you swap the design image.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"


def text_mask(img, box, v_min=105, s_max=90, cyan=False):
    x0, y0, x1, y1 = box
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, S, V = cv2.split(hsv)
    m = (V > v_min) & (S < s_max)
    if cyan:
        b, _, r = cv2.split(img.astype(int))
        m |= (b > 120) & (b - r > 40)
    out = np.zeros(V.shape, np.uint8)
    out[y0:y1, x0:x1] = (m[y0:y1, x0:x1] * 255).astype(np.uint8)
    return out


def remove_avatar(img):
    """Paint the round captain avatar out of the cover.

    Below the deck line the area is plain dark deck, so each row is rebuilt as a
    blend of the clean deck just left and right of the circle; the small cap that
    overlaps the crew is inpainted. Edges are feathered and a little grain added
    so the patch matches the painted texture.
    """
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    m = ((xx - 141) ** 2 + (yy - 251) ** 2 <= 93 ** 2) | ((xx - 201) ** 2 + (yy - 299) ** 2 <= 30 ** 2)
    m &= yy > 150
    out = img.astype(np.float32).copy()
    L, R = 34, 256
    for y in range(150, H):
        row = np.where(m[y])[0]
        if not len(row):
            continue
        cl = img[y, max(L - 6, 0):L].reshape(-1, 3).mean(0)
        cr = img[y, R:R + 6].reshape(-1, 3).mean(0)
        k = (row - L) / (R - L)
        out[y, row] = cl[None] * (1 - k[:, None]) + cr[None] * k[:, None]
    out = out.astype(np.uint8)
    cap = cv2.dilate((m & (yy < 214)).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    out = cv2.inpaint(np.where(cap[..., None] > 0, img, out).astype(np.uint8), cap, 6, cv2.INPAINT_TELEA)
    mm = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 4)[..., None]
    res = img * (1 - mm) + cv2.GaussianBlur(out, (0, 0), 1.6) * mm
    res += np.random.default_rng(1).normal(0, 2.2, res.shape) * mm
    return np.clip(res, 0, 255).astype(np.uint8)


def main(src: str) -> None:
    im = cv2.imread(src)
    OUT.mkdir(parents=True, exist_ok=True)
    hero = im[0:345, 0:1024].copy()

    mask = text_mask(hero, (250, 188, 705, 326), cyan=True)        # name, roles, tagline
    mask[188:226, 460:705] = 0                                      # keep the crew on the deck
    mask[196:230, 412:462] = 255                                    # little straw hat on the old name
    mask |= text_mask(hero, (28, 10, 212, 60), v_min=85, s_max=255)    # "Straw Hat Pirates" label
    mask[12:56, 30:80] = 255                                            # its skull logo
    mask |= text_mask(hero, (898, 12, 1004, 66), v_min=150, s_max=70)  # "Same Dream / Bigger Horizons"
    mask |= text_mask(hero, (880, 250, 990, 334), v_min=95, s_max=110) # "Dream Build Ship Repeat"
    mask |= text_mask(hero, (895, 290, 1000, 342), v_min=55, s_max=200) # ...and its pen swoosh
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    bg = cv2.inpaint(hero, mask, 9, cv2.INPAINT_TELEA)
    bg[232:330, 245:710] = cv2.GaussianBlur(bg[232:330, 245:710], (0, 0), 2.2)
    bg = remove_avatar(bg)
    cv2.imwrite(str(OUT / "hero.jpg"), bg, [cv2.IMWRITE_JPEG_QUALITY, 92])

    cv2.imwrite(str(OUT / "ship.jpg"), im[370:661, 410:987], [cv2.IMWRITE_JPEG_QUALITY, 90])
    cv2.imwrite(str(OUT / "city.jpg"), im[995:1178, 40:812], [cv2.IMWRITE_JPEG_QUALITY, 90])

    footer = im[1266:1536, 0:1024].copy()
    fm = np.zeros(footer.shape[:2], np.uint8)
    fm[56:92, 596:742] = 255       # old email chip
    fm[56:92, 84:346] = 255        # old GitHub + LinkedIn chips (the YouTube one sits under a new chip)
    cv2.imwrite(str(OUT / "footer.jpg"), cv2.inpaint(footer, fm, 12, cv2.INPAINT_TELEA), [cv2.IMWRITE_JPEG_QUALITY, 92])
    print("images written to", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
