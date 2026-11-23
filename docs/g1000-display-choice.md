# G1000 PFD/MFD display choice (2026-11-23)

## What the 737DIYSIM G1000 bezel is built around
Karl Clarke's G1000 Parts Guide specifies the **Toshiba LTD104EDZS**: 10.4 in, 1024x768 (4:3), LVDS, edge-lit LED.
* Outline about **219.1 x 173.8 x 2.6 mm** (6.3 mm max). Active area 210.4 x 157.8 mm.
* Source: [lcds-screen.com spec page](https://www.lcds-screen.com/products/LTD104EDZS_TOSHIBA_LCM_10.4-inch_1024x768_parameter.html). Verify against his STL pocket.
* The panel is out of production but sold widely as surplus/refurb with an HDMI driver board.

His MIP cutout for each G1000 is 282 x 179, so the bezel is narrower than a real GDU 1040 (about 300 mm). There's only about 31 mm per side for the knob/key columns. That's why he uses the narrow Toshiba panel.

## Chosen (2026-11-23): 2 x LTD104EDZS + HDMI controller board from AliExpress
**[AliExpress 1005011787148121](https://www.aliexpress.com/item/1005011787148121.html)**, YX-LCD Store, variant "LTD104EDZS-set1". C$72.38 each + C$3.76 shipping, qty 2 (about C$152 before tax). Listed as "Original New" and sold through AliExpress Choice with 90-day free returns. Added to BOM.md.

## eBay options compared before choosing
| Option | Price | Where | Notes |
|---|---|---|---|
| **LTD104EDZS + HDMI controller board** | US $69.99 each (or offer) | [eBay 396776434725](https://www.ebay.com/itm/396776434725) | Free SpeedPAK from Guangzhou, import fees included. Open box, "95% new, tested". 60-day returns |
| LTD104EDZS + HDMI/VGA/AV controller board | US $65.79 each (or offer) | [eBay 396776355883](https://www.ebay.com/itm/396776355883) | Same seller type and terms. VGA/AV are unused extras |

* About **CA $195–200 for the pair** delivered to Winnipeg.
* Power: these boards are normally 12 V. Use the case 12 V 5 A rail (already in the BOM) or a 12 V 2 A adapter each. Buyer feedback says cables or remotes are sometimes missing, so message the seller to confirm the LVDS cable, keypad and backlight cable are included before buying.
* No HDMI-input DisplayPort option exists for these surplus panels. Use HDMI from the PC (DP-to-HDMI adapters work fine).

## Alternatives, and why not
| Panel | Size | Verdict |
|---|---|---|
| AUO G104XVN01.0 (current production, our old MFD-1 spec) | 238.6 x 175.8 x 6.5. [RobotShop](https://www.robotshop.com/products/dualturb-auo-g104xvn010-104-industrial-high-resolution-xga-tft-lcd-display-module) US $160, panel only | Same 1024x768 picture, brighter (470 nits). But it's **about 20 mm wider** than the Toshiba, so it very likely won't fit his 282 mm bezel pocket. Needs a separate LVDS-HDMI board |
| Innolux G104X1-L03 + HDMI board | 238.6 x 175.8 x 7.5. [eBay 395637060447](https://www.ebay.com/itm/395637060447) US $62 | Same width problem as the AUO |
| Pimoroni PIM431 10 in kit (4:3, 1024x768, IPS) | 210.2 x 164.3 x 2.85, active 196.6 x 147.5. [RobotShop Canada](https://ca.robotshop.com/products/hdmi-10-lcd-screen-kit-1024x768) $215.29 each, 2 left | Fits in the pocket, ships from Canada, nice IPS panel. But the picture is about 7 mm smaller per side than his 210 x 158 window, so a black border shows unless the bezel window is reduced. Costs twice as much |
| Waveshare 10.1DP-CAPLCD (16:10, 1280x800) | about 217 x 136 active | 16:10 is the wrong shape. It's too short for the 158 mm-tall window and makes MSFS letterbox or stretch the G1000 pop-out |

## Open check
Measure the LCD pocket in his G1000 STL (inner width/height/depth) once the files are opened. If the pocket is 239 mm wide or more, the AUO becomes an option.
