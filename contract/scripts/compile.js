/**
 * Compiles contracts/GirihExe.sol with the real solc compiler and writes
 *   artifacts/GirihExe.abi.json
 *   artifacts/GirihExe.bytecode.txt
 * so the contract can be verified before anyone spends gas on it.
 */
const fs = require("fs");
const path = require("path");
const solc = require("solc");

const root = path.join(__dirname, "..");
const entry = "contracts/GirihExe.sol";

function normalize(p) {
  const parts = [];
  for (const seg of p.split("/")) {
    if (seg === "" || seg === ".") continue;
    if (seg === "..") parts.pop();
    else parts.push(seg);
  }
  return parts.join("/");
}

function findImports(p) {
  const rel = normalize(p);
  const candidates = [
    path.join(root, "node_modules", rel),
    path.join(root, rel),
    path.join(root, "node_modules", p),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return { contents: fs.readFileSync(c, "utf8") };
  }
  return { error: "not found: " + p };
}

const input = {
  language: "Solidity",
  sources: {
    [entry]: { content: fs.readFileSync(path.join(root, entry), "utf8") },
  },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    evmVersion: "cancun",
    outputSelection: {
      "*": { "*": ["abi", "evm.bytecode.object", "evm.deployedBytecode.object"] },
    },
  },
};

const out = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));

let fatal = false;
for (const e of out.errors || []) {
  if (e.severity === "error") fatal = true;
  console.log(`[${e.severity}] ${e.formattedMessage}`);
}

if (fatal) {
  console.log("\nCOMPILE FAILED");
  process.exit(1);
}

const contract = out.contracts[entry]["GirihExe"];
const art = path.join(root, "artifacts");
fs.mkdirSync(art, { recursive: true });
fs.writeFileSync(path.join(art, "GirihExe.abi.json"), JSON.stringify(contract.abi, null, 2));
fs.writeFileSync(path.join(art, "GirihExe.bytecode.txt"), contract.evm.bytecode.object);
fs.writeFileSync(
  path.join(art, "GirihExe.deployed.txt"),
  contract.evm.deployedBytecode.object
);

console.log(`\nCOMPILE OK  solc ${solc.version()}`);
console.log(`  functions : ${contract.abi.filter((x) => x.type === "function").length}`);
console.log(`  events    : ${contract.abi.filter((x) => x.type === "event").length}`);
console.log(`  bytecode  : ${contract.evm.bytecode.object.length / 2} bytes (creation)`);
console.log(`  artifacts : ${art}`);
