# B.Broth Shop

The online shop for **bbroth.asia** — a static site with a cart and a WhatsApp
checkout. No server, no database, no monthly bill.

Built for B.Broth (Omar and his wife's bone broth business). Deliberately shares
nothing with the SWIRL codebase or the B.Broth ERP; it is a separate deliverable
that happens to sell the same jars.

## Why static

GoDaddy's Websites + Marketing builder puts the online store behind a paid
Commerce plan, and GoDaddy Payments does not operate in Lebanon anyway — so the
subscription would have bought a card-checkout engine that could not be used.
Orders here go to WhatsApp instead, which is how the customers already buy, and
the whole thing hosts for free.

## Files

| Path | What it is |
|---|---|
| `index.html` | The entire site — markup, styles and cart logic in one file |
| `assets/` | Logos and photography (~560 KB total, already optimised) |
| `build_preview.py` | Inlines every asset into `preview_single_file.html` for sharing a preview link |
| `preview_single_file.html` | Generated. Not needed for deployment — do not edit by hand |

## Running it locally

```bash
python -m http.server 8099 --directory "C:\Users\User\OneDrive - brainbites\Desktop\BBROTH SHOP"
```

Then open <http://localhost:8099>. There is also a `bbroth-shop` preview config
in the SWIRL repo's `.claude/launch.json`, pointing here by absolute path — the
same pattern the `bbroth` ERP entry uses.

## Changing the shop

Everything a shopkeeper needs to change sits in the `<script>` block at the
bottom of `index.html`:

```js
const WA_NUMBER = "96171240389";   // where orders land
const MIN_ORDER = 6;               // USD
const ZONES = { beirut:{label:"Beirut", fee:3}, outside:{label:"Outside Beirut", fee:5} };
const PRODUCTS = [ /* id, name, Arabic name, price, image, specs, description */ ];
```

To add a product (a bundle, a bigger jar), append an entry to `PRODUCTS` and
drop a square image in `assets/`. Nothing else needs touching — the cards, the
cart and the WhatsApp message all read from that array.

Prices are plain numbers in USD. There is no tax handling, by design.

## How checkout works

1. Customer adds jars; the cart persists in `localStorage`.
2. They pick a delivery area, which sets the fee, and fill in name, phone and address.
3. The order is refused below the `MIN_ORDER` value, and again if name, phone or address is blank.
4. "Send order on WhatsApp" opens `wa.me/96171240389` with a pre-written,
   itemised order — quantities, subtotal, delivery, total, address and whether
   they are paying cash on delivery or by Whish.

Nothing is charged online. You confirm each order in the chat and collect on
delivery, so no payment gateway or merchant account is involved.

## Product data

Both jars are 250 g, 15-hour simmer, no preservatives, halal, GMO-free, shelf
stable for 12 months and good for 5 days refrigerated once opened. Nutrition and
ingredient copy on the site was transcribed from the printed label artwork
(`Bone Broth Jar Label Final ….pdf`), not invented.

> **Note for the next print run:** the physical label reads "protien" (protein)
> and "Tumeric" (turmeric). The website spells both correctly.

## Deploying to bbroth.asia

The domain is registered at GoDaddy; the site itself can be hosted free
elsewhere and pointed at that domain. Recommended: Cloudflare Pages — free
custom domains, automatic SSL, and good routing into Lebanon.

Roughly: create the Cloudflare account, upload this folder to a new Pages
project, add `bbroth.asia` as a custom domain, then change the nameservers on
the GoDaddy domain to the two Cloudflare gives you. Account creation and the
nameserver change have to be done by hand.

## Still to do

- Bundles / multi-jar pricing (deferred — decide the pricing first).
- Confirm the Instagram handle; the site links `@b.brothleb`, read off the label QR caption.
- Consider free delivery over a threshold — at a $6 minimum, a $3–5 delivery fee
  is a large share of a one-jar order and will suppress basket size.
