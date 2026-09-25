/**
 * Functional test: deploys GirihExe on an in-process EVM and exercises the
 * full sale lifecycle (pause, price, mint, sell-out, royalties, withdraw,
 * access control). Run with:  node scripts/test.js
 */
const fs = require("fs");
const path = require("path");
const ganache = require("ganache");
const { ethers } = require("ethers");

const root = path.join(__dirname, "..");
const abi = JSON.parse(fs.readFileSync(path.join(root, "artifacts/GirihExe.abi.json"), "utf8"));
const bytecode = "0x" + fs.readFileSync(path.join(root, "artifacts/GirihExe.bytecode.txt"), "utf8");

const PRICE = ethers.parseEther("0.05");
let IFACE = null;
let passed = 0;
let failed = 0;

function ok(cond, label) {
  if (cond) { passed++; console.log(`  PASS  ${label}`); }
  else { failed++; console.log(`  FAIL  ${label}`); }
}

/** Pull a human-readable reason out of a ganache/ethers revert (string or custom error). */
function reasonOf(e) {
  const info = (e.info && e.info.error) || {};
  const data = info.data || {};
  if (data.reason) return data.reason;
  let hex = data.result || data.data || e.data || (typeof e.data === "string" ? e.data : null);
  if (typeof hex === "string" && hex.startsWith("0x")) {
    if (IFACE) {
      try { const p = IFACE.parseError(hex); if (p) return p.name + "(" + p.args.join(",") + ")"; } catch (_) { /* fall through */ }
    }
    if (hex.startsWith("0x08c379a0")) {
      try { return ethers.AbiCoder.defaultAbiCoder().decode(["string"], "0x" + hex.slice(10))[0]; } catch (_) { /* ignore */ }
    }
    return hex;
  }
  return info.message || e.shortMessage || e.message || String(e);
}

async function expectRevert(promise, needle, label) {
  try { await promise; ok(false, label + " (did not revert)"); }
  catch (e) {
    const raw = reasonOf(e);
    const hit = String(raw).toLowerCase().includes(String(needle).toLowerCase());
    ok(hit, label + (hit ? "" : `  [got: ${String(raw).slice(0, 70)}]`));
  }
}

async function main() {
  const gProvider = ganache.provider({ logging: { quiet: true }, wallet: { totalAccounts: 5 } });
  const provider = new ethers.BrowserProvider(gProvider);
  const owner = await provider.getSigner(0);
  const buyer = await provider.getSigner(1);
  const buyer2 = await provider.getSigner(2);
  const payout = await provider.getSigner(3);
  const stranger = await provider.getSigner(4);

  const ownerAddr = await owner.getAddress();
  const buyerAddr = await buyer.getAddress();
  const payoutAddr = await payout.getAddress();

  console.log("\n1. deploy");
  const factory = new ethers.ContractFactory(abi, bytecode, owner);
  const c = await factory.deploy(PRICE, "ipfs://CID/");
  await c.waitForDeployment();
  IFACE = c.interface;
  const rawBalance = async (a) =>
    BigInt(await gProvider.request({ method: "eth_getBalance", params: [a, "latest"] }));
  ok(true, "deployed at " + (await c.getAddress()).slice(0, 18) + "...");
  ok((await c.name()) === "GIRIH.EXE" && (await c.symbol()) === "GIRIH", "name/symbol");
  ok((await c.MAX_SUPPLY()) === 10n, "MAX_SUPPLY = 10");
  ok((await c.mintPrice()) === PRICE, "mintPrice set by constructor");

  console.log("\n2. sale is paused by default");
  await expectRevert(c.connect(buyer).mint(1, { value: PRICE }), "sale is not active", "mint while paused reverts");
  ok((await c.totalSupply()) === 0n, "totalSupply still 0");

  const strangerAddr = await stranger.getAddress();

  console.log("\n3. owner config is protected");
  await expectRevert(c.connect(stranger).setSaleActive(true), "Ownable", "setSaleActive by stranger reverts");
  await expectRevert(c.connect(stranger).setMintPrice(0), "Ownable", "setMintPrice by stranger reverts");
  await expectRevert(c.connect(stranger).withdraw(strangerAddr), "Ownable", "withdraw by stranger reverts");
  await expectRevert(c.connect(stranger).ownerMint(1, ownerAddr), "Ownable", "ownerMint by stranger reverts");

  console.log("\n4. open the sale");
  await (await c.setSaleActive(true)).wait();
  ok((await c.saleActive()) === true, "saleActive = true");
  await expectRevert(c.connect(buyer).mint(1, { value: ethers.parseEther("0.01") }), "insufficient", "underpayment reverts");
  await expectRevert(c.connect(buyer).mint(0, { value: 0 }), "bad quantity", "quantity 0 reverts");
  await expectRevert(c.connect(buyer).mint(11, { value: ethers.parseEther("0.55") }), "bad quantity", "quantity 11 reverts");

  console.log("\n5. buyers mint");
  await (await c.connect(buyer).mint(3, { value: ethers.parseEther("0.15") })).wait();
  ok((await c.totalSupply()) === 3n, "3 minted");
  ok((await c.ownerOf(1)) === buyerAddr && (await c.ownerOf(3)) === buyerAddr, "ownerOf 1..3 = buyer");
  ok((await c.tokenURI(2)) === "ipfs://CID/2", "tokenURI = base + id");

  const rest = 10 - 3;
  await expectRevert(c.connect(buyer2).mint(rest + 1, { value: PRICE * BigInt(rest + 1) }), "sold out", "minting past MAX_SUPPLY reverts");
  await (await c.connect(buyer2).mint(rest, { value: PRICE * BigInt(rest) })).wait();
  ok((await c.totalSupply()) === 10n, "totalSupply = 10 (sold out)");
  await expectRevert(c.connect(buyer).mint(1, { value: PRICE }), "sold out", "mint after sell-out reverts");

  console.log("\n6. royalties (ERC-2981)");
  const [rAddr, rFee] = await c.royaltyInfo(1, 10000n);
  ok(rFee === 500n, "5% royalty (500 bps of 10000)");
  ok(rAddr === ownerAddr, "royalty receiver = deployer");

  console.log("\n7. money and payout");
  const addr = await c.getAddress();
  const bal = await rawBalance(addr);
  ok(bal === ethers.parseEther("0.50"), "contract holds 0.50 ETH (10 x 0.05)");
  const payoutBefore = await rawBalance(payoutAddr);
  await (await c.withdraw(payoutAddr)).wait();
  ok((await rawBalance(addr)) === 0n, "contract emptied");
  ok((await rawBalance(payoutAddr)) - payoutBefore === ethers.parseEther("0.50"), "payout wallet received 0.50 ETH");

  console.log("\n8. metadata / royalties can be re-pointed by owner only");
  await (await c.setBaseURI("ipfs://SECOND/")).wait();
  ok((await c.tokenURI(1)) === "ipfs://SECOND/1", "setBaseURI works");
  await (await c.setRoyalty(payoutAddr, 750)).wait();
  const [, f2] = await c.royaltyInfo(1, 10000n);
  ok(f2 === 750n, "setRoyalty works (7.5%)");
  await expectRevert(c.connect(stranger).setBaseURI("ipfs://X/"), "Ownable", "setBaseURI by stranger reverts");

  console.log(`\n===== ${passed} passed, ${failed} failed =====\n`);
  await gProvider.disconnect();
  process.exit(failed === 0 ? 0 : 1);
}

main().catch((e) => { console.error(e); process.exit(1); });
