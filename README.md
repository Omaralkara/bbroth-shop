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
const FREE_DELIVERY = 24;          // subtotal at or above this ships free
const ZONES = { beirut:{label:"Beirut", fee:3}, outside:{label:"Outside Beirut", fee:5} };
const PRODUCTS = [ /* id, name, Arabic name, price, image, specs, description */ ];
```

To add a product (a bundle, a bigger jar), append an entry to `PRODUCTS` and
drop a square image in `assets/`. Nothing else needs touching — the cards, the
cart and the WhatsApp message all read from that array.

Prices are plain numbers in USD. There is no tax handling, by design.

## How checkout works

1. Customer adds jars; the cart persists in `localStorage`.
2. They pick a delivery area, which sets the fee — waived entirely once the
   subtotal reaches `FREE_DELIVERY` — and fill in name, phone and address. A
   progress bar in the cart shows how much more is needed to earn it.
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

> **Notes for the next print run.** The physical label reads "protien"
> (protein) and "Tumeric" (turmeric); the website spells both correctly.
>
> The beef label disagrees with itself: the front panel says **18 g protein per
> jar** while the nutrition panel says **6 g per 100 g serving**, which over 2.5
> servings comes to 15 g. On Omar's instruction the site transcribes both
> printed figures exactly as they appear on the sticker rather than reconciling
> them, so the website always matches the jar in the customer's hand. Fix the
> panel at the next print run and update `index.html` to match. Chicken is
> already consistent at 20 g per jar / 8 g per serving.

## Deployment

Live at **https://bbroth.asia**, served by GitHub Pages from the `master`
branch of `Omaralkara/bbroth-shop`. Push to `master` and the change is live in
about a minute — there is no build step, the repository root is the site.

The `CNAME` file at the root holds the custom domain; do not delete it.

DNS lives at GoDaddy. The apex `A` records point at GitHub Pages:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |

GitHub publishes four Pages addresses; only two are set here, which is enough
to serve. Adding `185.199.110.153` and `185.199.111.153` as further `A` records
on `@` would buy a little redundancy. The `www` CNAME, nameservers and the
`_dmarc` TXT record were left as GoDaddy had them.

HTTPS is enforced and the certificate renews itself.

## Email signatures

`assets/email/signature-logo.png` is loaded live by the team's email
signatures — mail clients will not embed images, so every sent email fetches
it from bbroth.asia. **Do not rename, move or delete it**, or the logo breaks
in every signature already in use. Replace the file in place to update it.

## Card payments

`CARD_PAYMENT` in `index.html` is `false`, so checkout offers cash on delivery
and Whish only. Setting it to `true` adds a "Pay by card" option that flags the
WhatsApp order for a payment link — but only turn it on once a provider that
operates in Lebanon is actually in place. Stripe and PayPal do not onboard
Lebanese merchants; the workable routes are Whish Business, Areeba, or Tap
Payments. Shelved for now by Omar's decision.

## Still to do

- Bundles / multi-jar pricing (deferred — decide the pricing first).
- Confirm the Instagram handle; the site links `@b.brothleb`, read off the label QR caption.
- Optionally add the two remaining GitHub Pages A records.
