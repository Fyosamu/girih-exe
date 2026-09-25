# Contract test run

Environment: ganache (in-process) + ethers, solc 0.8.24, OpenZeppelin 5.6.1

Commands:

\\nnpm.cmd run compile
node scripts/test.js
\\n
Output:

\\nThis version of µWS is not compatible with your Node.js build:

Error: Cannot find module '../binaries/uws_win32_x64_127.node'
Require stack:
- C:\Users\USER\Documents\Default Project\nft-collection\contract\node_modules\ganache\node_modules\@trufflesuite\uws-js-unofficial\src\uws.js
- C:\Users\USER\Documents\Default Project\nft-collection\contract\node_modules\ganache\dist\node\core.js
- C:\Users\USER\Documents\Default Project\nft-collection\contract\scripts\test.js
Falling back to a NodeJS implementation; performance may be degraded.



1. deploy
  PASS  deployed at 0x73832f6a21D5e263...
  PASS  name/symbol
  PASS  MAX_SUPPLY = 10
  PASS  mintPrice set by constructor

2. sale is paused by default
  PASS  mint while paused reverts
  PASS  totalSupply still 0

3. owner config is protected
  PASS  setSaleActive by stranger reverts
  PASS  setMintPrice by stranger reverts
  PASS  withdraw by stranger reverts
  PASS  ownerMint by stranger reverts

4. open the sale
  PASS  saleActive = true
  PASS  underpayment reverts
  PASS  quantity 0 reverts
  PASS  quantity 11 reverts

5. buyers mint
  PASS  3 minted
  PASS  ownerOf 1..3 = buyer
  PASS  tokenURI = base + id
  PASS  minting past MAX_SUPPLY reverts
  PASS  totalSupply = 10 (sold out)
  PASS  mint after sell-out reverts

6. royalties (ERC-2981)
  PASS  5% royalty (500 bps of 10000)
  PASS  royalty receiver = deployer

7. money and payout
  PASS  contract holds 0.50 ETH (10 x 0.05)
  PASS  contract emptied
  PASS  payout wallet received 0.50 ETH

8. metadata / royalties can be re-pointed by owner only
  PASS  setBaseURI works
  PASS  setRoyalty works (7.5%)
  PASS  setBaseURI by stranger reverts

===== 28 passed, 0 failed =====
\\n