# GIRIH.EXE — بسته‌ی کاملِ ۱۰ NFT برای فروش

> ده اثر تولیدی (Generative) از هندسه‌ی ایرانی/گره‌چینی، همراهِ قرارداد هوشمندِ **تست‌شده**، متادیتای استاندارد و متنِ آماده‌ی فروش.

---

## ۱) محتویات این پوشه

| مسیر | چیست |
|---|---|
| `output/1.png … 10.png` | خودِ آثار — ۱۰۲۴×۱۰۲۴، آماده‌ی آپلود |
| `metadata/1.json … 10.json` | متادیتای استاندارد ERC-721 (OpenSea-compatible) |
| `metadata/contract.json` | متادیتای سطح مجموعه (برای `contractURI`) |
| `collection.json` | آمار ترکیت‌ها + نادر بودن هر صفت |
| `generate.py` | مولدِ آثار — با همان `SEED` دقیقاً همین خروجی را می‌سازد |
| `_contact_sheet.png` | برگه‌ی نمایشیِ هر ۱۰ اثر در کنار هم |
| `contract/` | قرارداد Solidity + کامپایل + **۲۸ تست عملکردی** |
| `SALES.md` | متنِ فروش (انگلیسی/فارسی)، قیمت‌گذاری، محل‌های فروش |

---

## ۲) آثار

هر توکن از این صفت‌ها تشکیل شده است (تعیین‌شده با بذر/seed — تکرارپذیر):

- **Pattern** — 8-Point Star Rosette / Interlaced 10-Star / Hexagonal Lattice / 12-Point Khatam / Radial Burst
- **Palette** — Midnight Gold / Neon Bazaar / Emerald Prayer / Solar Tile / Ice Mosque
- **Density** — Sparse / Balanced / Dense
- **Aura** — Bloom / Grain / Scanline
- **Accent** و **Finish**

تولید مجدد (دقیقاً همان خروجی):

```powershell
cd nft-collection
python generate.py
```

---

## ۳) قرارداد هوشمند

- **نام/نماد:** `GIRIH.EXE` / `GIRIH`
- **سقف عرضه:** دقیقاً ۱۰ (`MAX_SUPPLY`)
- **استاندارد:** ERC-721 + متادیتای on-chain-URI + **ERC-2981** (امتیاز ۵٪ پیش‌فرض)
- **کنترل:** فقط مالک (`Ownable`) می‌تواند فروش را باز/بسته کند، قیمت را عوض کند، متادیتا را جابه‌جا کند و برداشت کند
- **برداشت:** `withdraw(to)` کل مبلغ قرارداد را به آدرسِ دلخواه (مثلاً آدرس Trust Wallet شما) می‌فرستد

### کامپایل و تست (قبل از خرج کردنِ حتی یک گاز)

```powershell
cd nft-collection/contract
npm install
npm run compile        # COMPILE OK با solc 0.8.24
node scripts/test.js   # ===== 28 passed, 0 failed =====
```

تست‌ها این‌ها را پوشش می‌دهند: بسته‌بودنِ فروش، کنترل دسترسیِ غیرمالک، کم‌پرداختی، کوانتیتای نامعتبر، سقفِ ۱۰ تا، `tokenURI`، امتیاز ۵٪، موجودیِ دقیقِ قرارداد، و واریزِ کامل به کیف پول.

> این تست‌ها یک **باگ واقعی** را هم پیدا و رفع کردند: `ERC721URIStorage` خودش پایه‌ی URI را جلوی شناسه می‌گذارد؛ ذخیره‌ی `base + id` باعث می‌شد آدرس دوبار تکرار شود.

### خروجی‌ها

`contract/artifacts/` شامل `GirihExe.abi.json` و `GirihExe.bytecode.txt` است — همان چیزی که برای Remix یا هر اسکریپت استقرار لازم دارید.

---

## ۴) مراحل انتشار (قدم‌به‌قدم)

> ⚠️ **هرگز عبارت بازیابی (Seed) یا کلید خصوصی را به هیچ‌کس — از جمله من — ندهید.**
> امضای تراکنش فقط و فقط باید در کیف پول خودتان انجام شود.

### قدم ۱ — آپلود روی IPFS

هر ۱۰ تصویر + ۱۰ فایل `metadata` + `contract.json` را روی IPFS پین کنید.
گزینه‌های رایگان/ارزان: **Pinata**، **Filebase**، **NFT.Storage**، **web3.storage**.

دو نتیجه لازم دارید:
- `TOKENS_CID` — پوشه‌ای که `1.png … 10.json` داخلش است → برای `setBaseURI("ipfs://TOKENS_CID/")`
- `CONTRACT_CID` — فایل `contract.json` → برای `contractURI`

> نکته: فایل‌های متادیتا به `image` اشاره دارند و الان مقدار placeholder دارند
> (`ipfs://REPLACE_CID/1.png`). بعد از آپلودِ تصاویر، با یک جایگزینی سراسری CID را بگذارید.

### قدم ۲ — استقرار قرارداد

**روش A — Remix (ساده‌ترین، بدون خط فرمان):**
1. [remix.ethereum.org](https://remix.ethereum.org) → قرارداد `GirihExe.sol` را در کنار `node_modules/@openzeppelin/contracts` کپی کنید (یا همان فایل را با دقت در Remix باز کنید).
2. در تب Compile، نسخه‌ی `0.8.24` را انتخاب کنید → Compile.
3. در تب Deploy، کیف پولتان را وصل کنید، آرگومان‌ها را بدهید:
   - `mintPrice_` = قیمت هر توکن به **Wei** (مثلاً `50000000000000000` برای ۰٫۰۵ ETH)
   - `baseURI_` = `ipfs://TOKENS_CID/` (یا بعداً از طریق `setBaseURI` )
4. Deploy و تأیید در کیف پول.

**روش B — اسکریپت:**

```powershell
cd nft-collection/contract
# کلید خصوصی را فقط در همین ترمینالِ محلی وارد کنید؛ آن را برایم نفرستید
$env:RPC_URL     = "https://bsc-dataseed.binance.org"
$env:PRIVATE_KEY = "0x..."
node scripts/deploy.js
```

**شبکه پیشنهادی:** به‌خاطر هزینه‌ی کم، **BNB Chain** یا **Polygon** یا **Base**.
(قرارداد EVM است و روی همه‌ی این‌ها کار می‌کند.)

### قدم ۳ — راه‌اندازی فروش

```text
setBaseURI("ipfs://TOKENS_CID/")
setRoyalty(آدرس شما, 500)      # 5% — پیش‌فرض هم همین است
setSaleActive(true)
```

### قدم ۴ — تأیید روی بلاک‌اکسپلورر

کد منبع را در Etherscan/BscScan/Polygonscan با همان `solc 0.8.24` و
`@openzeppelin/contracts 5.6.1` و Optimizer=200 تأیید کنید تا خریدارها بتوانند کد را بخوانند
(این‌ها برای اعتمادسازیِ فروش خیلی مهم است).

---

## ۵) خلاصه‌ی وضعیت

| مرحله | وضعیت |
|---|---|
| ساخت ۱۰ اثر | ✅ انجام شد |
| متادیتای ۱۰ توکن + مجموعه | ✅ انجام شد |
| قرارداد هوشمند | ✅ نوشته شد |
| کامپایل | ✅ `COMPILE OK` (solc 0.8.24) |
| تست عملکردی | ✅ **28 passed / 0 failed** |
| آپلود IPFS | ⬜ نیاز به حساب شما (Pinata/…) |
| استقرار | ⬜ نیاز به **امضای کیف پول شما** |
| اتصال به بازارچه | ⬜ نیاز به ورود شما (کیف پول) |
