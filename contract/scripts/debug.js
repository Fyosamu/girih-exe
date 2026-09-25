const fs = require("fs");
const path = require("path");
const ganache = require("ganache");
const { ethers } = require("ethers");

const root = path.join(__dirname, "..");
const abi = JSON.parse(fs.readFileSync(path.join(root, "artifacts", "GirihExe.abi.json"), "utf8"));
const bytecode = "0x" + fs.readFileSync(path.join(root, "artifacts", "GirihExe.bytecode.txt"), "utf8");

async function main() {
  const gp = ganache.provider({ logging: { quiet: true } });
  const provider = new ethers.BrowserProvider(gp);
  const owner = await provider.getSigner(0);
  const buyer = await provider.getSigner(1);
  const f = new ethers.ContractFactory(abi, bytecode, owner);
  const c = await f.deploy(ethers.parseEther("0.05"), "ipfs://CID/");
  await c.waitForDeployment();

  // --- tokenURI debug
  await (await c.setSaleActive(true)).wait();
  await (await c.connect(buyer).mint(2, { value: ethers.parseEther("0.10") })).wait();
  const tu = await c.tokenURI(1);
  console.log("tokenURI(1) =", JSON.stringify(tu), "type:", typeof tu);

  // --- revert reason debug
  try {
    await c.connect(buyer).mint(1, { value: ethers.parseEther("0.01") });
    console.log("underpayment did NOT revert");
  } catch (e) {
    console.log("--- underpayment error ---");
    console.log("keys:", Object.keys(e));
    console.log("message:", (e.message || "").slice(0, 160));
    console.log("shortMessage:", (e.shortMessage || "").slice(0, 160));
    console.log("data:", e.data);
    console.log("info.error:", e.info && e.info.error);
    console.log("error.data:", e.error && e.error.data);
    console.log("cause:", e.cause && (e.cause.data || e.cause.message || ""));
  }

  // raw eth_call to see what ganache returns
  const data = c.interface.encodeFunctionData("mint", [1]);
  try {
    const raw = await gp.request({ method: "eth_call", params: [{ to: await c.getAddress(), data, from: await (await provider.getSigner(1)).getAddress() }, "latest"] });
    console.log("raw eth_call result:", raw);
  } catch (e) {
    console.log("raw eth_call error:", JSON.stringify(e, null, 2).slice(0, 800));
  }

  await gp.disconnect();
}

main().catch((e) => { console.error("FATAL", e); process.exit(1); });
