# SALES — متن‌ها و استراتژی فروشِ GIRIH.EXE

> این فایل «چیزی است که باید کپی/پیست کنید». تمام متن‌های زیر آماده‌اند؛
> فقط `REPLACE`ها را با آدرس واقعی پر کنید.

---

## ۱) معرفی کوتاه (انگلیسی) — برای بازارچه

**Name:** GIRIH.EXE
**Description:**

> Ten generative artworks built from Persian girih geometry — star rosettes,
> interlaced decagrams and khatam lattice — rendered as neon-lit digital tiles.
>
> Every line is computed from a seed; nothing is drawn by hand. Each piece carries
> six independent traits (pattern, palette, density, aura, accent, finish), so no two
> of the ten are alike. 1024×1024 PNG, ERC-721, ERC-2981 royalties, fixed supply of 10.
>
> Artist's note: girih is the geometric system that underlies the tilework of Persian
> architecture. This collection re-runs that logic on a GPU instead of a plaster wall.

**Tags:** generative art, geometric, persian, islamic geometry, girih, algorithmic art, minimal, neon

---

## ۲) معرفی کوتاه (فارسی) — برای کانال‌ها و شبکه‌های اجتماعی

> **GIRIH.EXE** — ده اثر تولیدی از هندسه‌ی ایرانی
>
> هر خط با یک الگوریتم و یک بذر محاسبه شده؛ هیچ‌کدام دستی کشیده نشده.
> ستاره‌های چندپر، شبکه‌های خاتم و نقش‌های چندوجهی — با نورِ نئونی روی زمینه‌ی تیره.
>
> شش صفت مستقل (الگو، رنگ، تراکم، هاله، لهجه، پرداخت) باعث می‌شود هیچ دو تا شبیه هم نباشند.
> عرضه محدود: **فقط ۱۰ عدد.** استاندارد ERC-721، امتیاز فروش مجدد ۵٪.
>
> نمونه‌ها: `REPLACE_LINK`
> خرید: `REPLACE_MARKETPLACE_LINK`

---

## ۳) قیمت‌گذاری (پیشنهاد)

| سناریو | قیمت هر عدد | یادداشت |
|---|---|---|
| **شروع (پیشنهاد)** | ۰٫۰۲–۰٫۰۵ ETH/BNB | برای جذبِ ۲-۳ خریدار اول؛ سیگنال «ارزان نیست» |
| بالا | ۰٫۱ ETH | فقط اگر از قبل مخاطب دارید |
| ایرانی/غیر NFTمحور | ۱۵–۴۰ USDT | برای فروش به خریدار ایرانی، USDT طبیعی‌تر است |

**نکته‌ی مهم:** عرضه‌های ۱۰تایی به‌ندرت کامل فروخته می‌شوند. پس:
- اول **۲ عدد** را با قیمت کمتر بفروشید تا سابقه‌ی معامله روی مجموعه ثبت شود
- بعد قیمت را بالا ببرید (`setMintPrice`)
- فشار را روی «کمیابی واقعی» بگذارید: ۱۰ تا و بیشتر نداریم

**پرداخت خریدار:** با کیف پول روی شبکه (ETH/BNB/MATIC).
**پول شما:** با `withdraw(آدرس Trust Wallet شما)` به ولت خودتان می‌رود.

---

## ۴) کجا بفروشیم (ترتیب پیشنهادی)

| اولویت | بازارچه | چرا | نیازمندی |
|---|---|---|---|
| ۱ | **OpenSea** | بزرگ‌ترین ورودی خریدار | اتصال کیف پول + آپلود مجموعه (رایگان) |
| ۲ | **Rarible** | قابلیت ساخت مجموعه بدون کارمزد انتشار | اتصال کیف پول |
| ۳ | **Magic Eden** | خوب برای Base/Polygon/Solana | اتصال کیف پول |
| ۴ | **sudoswap / Fresco** | فروش مستقیم | اتصال کیف پول |
| ۵ | مستقیم از سایت خودتان | ۱۰۰٪ سود، بدون کارمزد واسطه | دکمه‌ی خرید روی `fyosamu.github.io` |

**قدم‌ها (OpenSea):**
1. کیف پول را وصل کنید → Create → All NFTs → Add New Items
2. هر ۱۰ تصویر را آپلود کنید و فیلدهای متادیتا را از `metadata/*.json` کپی کنید
   (Pattern / Palette / Density / Aura / Accent / Finish)
3. Supply را `1` بگذارید (هر کدام فقط یک عدد)
4. Create Collection → کارمزد فروش را ۵٪ بگذارید (با ERC-2981 یکی می‌شود)
5. لینک مجموعه را بگیرید

> اگر قرارداد خودتان را مستقر کرده‌اید، در OpenSea گزینه‌ی
> **«Use an existing contract»** را بزنید و آدرس قرارداد را بدهید تا توکن‌ها
> از همان‌جا خوانده شوند.

---

## ۵) معرفی برای شبکه‌های اجتماعی (آماده‌ی کپی)

**X / Twitter:**

> GIRIH.EXE — 10 generative pieces of Persian girih geometry, computed line by line.
> Six traits, fixed supply of 10, ERC-721.
> Not a drop. A tile.
> 🖼 REPLACE_LINK

**Reddit (r/NFT, r/generative, r/GenerativeArt):**

> Title: I re-ran Persian girih geometry on a GPU — 10 pieces, fixed supply
> Body: Girih is the geometric system behind Persian tilework. I wrote a generator
> that lays it out from a seed, then rendered each piece with a bloom pass.
> Six independent traits per piece, 1024px, ERC-721, only 10 exist.
> Link: REPLACE_LINK

**فارسی (کانال/اینستاگرام/توییتر فارسی):**

> ده اثر از هندسه‌ی ایرانی، تولیدشده با الگوریتم — فقط ۱۰ عدد، برای همیشه.
> نمونه‌ها: REPLACE_LINK

**هش‌تگ‌ها:**
`#GenerativeArt #Girih #PersianArt #IslamicGeometry #NFTCollection #AlgorithmicArt`
`#هنر_ایرانی #هندسه`

---

## ۶) واقع‌بینانه (بخشی که هیچ‌کس نمی‌گوید)

1. **بازار NFT الان راکد است.** احتمال فروخته‌شدنِ خودبه‌خودِ ۱۰ عدد بدون مخاطب، پایین است.
   ارزش واقعی این بسته: نمونه‌کارِ قابل‌نمایش + قابلیت تکرار برای هر مجموعه‌ی بعدی.
2. **کلید فروش، داستان است** نه تصویر. جمله‌ی «هندسه‌ی کاشی‌ای ایرانی، دوباره اجرا شده روی GPU»
   خیلی قوی‌تر از «۱۰ عدد NFT زیبا» است.
3. **اگر فروش رفت:** همان ژنراتور با `SEED` دیگر می‌تواند مجموعه‌ی ۱۰۰تایی بسازد —
   کافی است `TOTAL` را عوض کنید.
4. **هزینه‌ی واقعی:** IPFS (رایگان تا چند صد مگابایت) + گاز استقرار
   (روی BNB/Polygon معمولاً زیر ۱ دلار؛ روی Ethereum چند ده دلار).

---

## ۷) چک‌لیست نهایی قبل از اعلام فروش

- [ ] ۱۰ تصویر روی IPFS پین شد
- [ ] CID داخل هر `metadata/*.json` و `contract.json` جایگزین شد
- [ ] قرارداد مستقر شد
- [ ] `setBaseURI` و `setSaleActive(true)` اجرا شد
- [ ] قرارداد روی بلاک‌اکسپلورر تأیید (Verify) شد
- [ ] یک خریدار آزمایشی از خودتان خرید کرد و `tokenURI` درست باز شد
- [ ] لینک مجموعه در سایت خودتان گذاشته شد
- [ ] پست معرفی منتشر شد (حداقل X + یک سابردیت + یک کانال فارسی)
