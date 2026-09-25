// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title GIRIH.EXE
 * @notice A closed collection of exactly 10 generative artworks built from
 *         Persian girih geometry. Fully on-chain ownership; metadata lives on IPFS.
 *
 * Deploy once, then:
 *   1. setBaseURI("ipfs://<CID>/")            after the metadata folder is pinned
 *   2. setSaleActive(true)
 *   3. collect with mint(); withdraw() pays out to your own wallet
 *
 * The deployer/signer is the owner. Nobody except the owner can mint, price,
 * pause, re-point metadata or move funds.
 */
contract GirihExe is ERC721URIStorage, ERC2981, Ownable, ReentrancyGuard {
    using Strings for uint256;

    uint256 public constant MAX_SUPPLY = 10;
    uint256 public constant MAX_PER_TX = 10;

    uint256 public totalSupply;
    uint256 public mintPrice;
    bool public saleActive;

    string private _baseTokenURI;

    event SaleActiveSet(bool active);
    event MintPriceSet(uint256 price);
    event BaseURISet(string baseURI);
    event RoyaltySet(address indexed receiver, uint96 feeNumerator);
    event Withdrawn(address indexed to, uint256 amount);

    constructor(uint256 mintPrice_, string memory baseURI_)
        ERC721("GIRIH.EXE", "GIRIH")
        Ownable(msg.sender)
    {
        mintPrice = mintPrice_;
        _baseTokenURI = baseURI_;
        _setDefaultRoyalty(msg.sender, 500); // 5% royalty, in basis points
    }

    // ---------------------------------------------------------------- minting

    /// @notice Public mint. Requires the sale to be active and exact-or-higher payment.
    function mint(uint256 quantity) external payable nonReentrant {
        require(saleActive, "GirihExe: sale is not active");
        _checkQuantity(quantity);
        require(msg.value >= mintPrice * quantity, "GirihExe: insufficient payment");
        _batchMint(quantity, msg.sender);
    }

    /// @notice Owner can always mint outside the sale (airdrops, team reserve).
    function ownerMint(uint256 quantity, address to) external onlyOwner nonReentrant {
        _checkQuantity(quantity);
        _batchMint(quantity, to);
    }

    function _checkQuantity(uint256 quantity) internal pure {
        require(quantity > 0 && quantity <= MAX_PER_TX, "GirihExe: bad quantity");
    }

    function _batchMint(uint256 quantity, address to) internal {
        require(totalSupply + quantity <= MAX_SUPPLY, "GirihExe: sold out");
        require(bytes(_baseTokenURI).length > 0, "GirihExe: base URI not set");
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = ++totalSupply;
            _safeMint(to, tokenId);
            // ERC721URIStorage prepends _baseURI() itself, so we store only the id
            _setTokenURI(tokenId, tokenId.toString());
        }
    }

    // ------------------------------------------------------------ owner config

    function setSaleActive(bool active) external onlyOwner {
        saleActive = active;
        emit SaleActiveSet(active);
    }

    function setMintPrice(uint256 price) external onlyOwner {
        mintPrice = price;
        emit MintPriceSet(price);
    }

    /// @dev Called after images + metadata are uploaded to IPFS, e.g. "ipfs://bafy.../"
    function setBaseURI(string calldata baseURI_) external onlyOwner {
        _baseTokenURI = baseURI_;
        emit BaseURISet(baseURI_);
    }

    function setRoyalty(address receiver, uint96 feeNumerator) external onlyOwner {
        _setDefaultRoyalty(receiver, feeNumerator);
        emit RoyaltySet(receiver, feeNumerator);
    }

    /// @notice Sends the whole contract balance to your wallet (e.g. Trust Wallet address).
    function withdraw(address payable to) external onlyOwner nonReentrant {
        require(to != address(0), "GirihExe: zero address");
        uint256 amount = address(this).balance;
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "GirihExe: transfer failed");
        emit Withdrawn(to, amount);
    }

    // ------------------------------------------------------------------ views

    function walletOfOwner(address owner_) external view returns (uint256[] memory) {
        uint256 count;
        for (uint256 i = 1; i <= totalSupply; i++) {
            if (ownerOf(i) == owner_) count++;
        }
        uint256[] memory tokens = new uint256[](count);
        uint256 k;
        for (uint256 i = 1; i <= totalSupply; i++) {
            if (ownerOf(i) == owner_) tokens[k++] = i;
        }
        return tokens;
    }

    function contractURI() external pure returns (string memory) {
        // marketplaces such as OpenSea read this for collection-level metadata
        return "ipfs://REPLACE_CONTRACT_METADATA_CID/contract.json";
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
