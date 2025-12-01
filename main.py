"""
Solana Token Transfer Tool
Supports both SOL and USDC transfers on Solana blockchain
"""
import os
import argparse
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solders.instruction import Instruction, AccountMeta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Token Program ID
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
# Associated Token Program ID  
ASSOCIATED_TOKEN_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
# USDC Token Mint Address (mainnet)
USDC_MINT_ADDRESS = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def transfer_sol(to_address: str, amount: float) -> str:
    """
    Transfer SOL tokens to a specified address
    
    Args:
        to_address: Recipient's Solana address
        amount: Amount of SOL to transfer (in SOL, not lamports)
    
    Returns:
        Transaction signature
    """
    # Load private key from environment
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env file")
    
    # Load RPC URL
    rpc_url = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Initialize client
    client = Client(rpc_url)
    
    # Create keypair from private key (Base58 format)
    sender_keypair = Keypair.from_base58_string(private_key)
    
    # Convert recipient address to Pubkey
    recipient_pubkey = Pubkey.from_string(to_address)
    
    # Convert SOL to lamports (1 SOL = 1_000_000_000 lamports)
    lamports = int(amount * 1_000_000_000)
    
    # Create transfer instruction
    transfer_ix = transfer(
        TransferParams(
            from_pubkey=sender_keypair.pubkey(),
            to_pubkey=recipient_pubkey,
            lamports=lamports
        )
    )
    
    # Get recent blockhash
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    
    # Create and sign transaction
    message = Message.new_with_blockhash(
        [transfer_ix],
        sender_keypair.pubkey(),
        recent_blockhash
    )
    transaction = Transaction([sender_keypair], message, recent_blockhash)
    
    # Send transaction
    result = client.send_transaction(transaction)
    signature = str(result.value)
    
    print(f"✅ SOL transfer successful!")
    print(f"   From: {sender_keypair.pubkey()}")
    print(f"   To: {to_address}")
    print(f"   Amount: {amount} SOL")
    print(f"   Signature: {signature}")
    print(f"   Explorer: https://solscan.io/tx/{signature}")
    
    return signature


def get_associated_token_address(owner: Pubkey, mint: Pubkey) -> Pubkey:
    """
    Get the associated token account address for a wallet and mint
    """
    # Find PDA for associated token account
    seeds = [
        bytes(owner),
        bytes(TOKEN_PROGRAM_ID),
        bytes(mint),
    ]
    
    pda, _ = Pubkey.find_program_address(seeds, ASSOCIATED_TOKEN_PROGRAM_ID)
    return pda


def create_transfer_checked_instruction(
    source: Pubkey,
    mint: Pubkey,
    destination: Pubkey,
    owner: Pubkey,
    amount: int,
    decimals: int,
) -> Instruction:
    """
    Create a TransferChecked instruction for SPL Token
    """
    # TransferChecked instruction discriminator is 12
    data = bytes([12]) + amount.to_bytes(8, 'little') + bytes([decimals])
    
    keys = [
        AccountMeta(pubkey=source, is_signer=False, is_writable=True),
        AccountMeta(pubkey=mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=destination, is_signer=False, is_writable=True),
        AccountMeta(pubkey=owner, is_signer=True, is_writable=False),
    ]
    
    return Instruction(TOKEN_PROGRAM_ID, data, keys)


def transfer_usdc(to_address: str, amount: float) -> str:
    """
    Transfer USDC tokens to a specified address
    
    Args:
        to_address: Recipient's Solana address
        amount: Amount of USDC to transfer (in USDC, not smallest unit)
    
    Returns:
        Transaction signature
    """
    # Load private key from environment
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env file")
    
    # Load RPC URL
    rpc_url = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Use USDC mint address
    usdc_mint_str = USDC_MINT_ADDRESS
    
    # Initialize client
    client = Client(rpc_url)
    
    # Create keypair from private key
    sender_keypair = Keypair.from_base58_string(private_key)
    
    # Convert addresses to Pubkey
    recipient_pubkey = Pubkey.from_string(to_address)
    usdc_mint_pubkey = Pubkey.from_string(usdc_mint_str)
    
    # Get associated token accounts
    sender_token_account = get_associated_token_address(sender_keypair.pubkey(), usdc_mint_pubkey)
    recipient_token_account = get_associated_token_address(recipient_pubkey, usdc_mint_pubkey)
    
    # USDC has 6 decimals
    decimals = 6
    amount_in_smallest_unit = int(amount * (10 ** decimals))
    
    # Create transfer instruction
    transfer_ix = create_transfer_checked_instruction(
        source=sender_token_account,
        mint=usdc_mint_pubkey,
        destination=recipient_token_account,
        owner=sender_keypair.pubkey(),
        amount=amount_in_smallest_unit,
        decimals=decimals,
    )
    
    # Get recent blockhash
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    
    # Create and sign transaction
    message = Message.new_with_blockhash(
        [transfer_ix],
        sender_keypair.pubkey(),
        recent_blockhash
    )
    transaction = Transaction([sender_keypair], message, recent_blockhash)
    
    # Send transaction
    result = client.send_transaction(transaction)
    signature = str(result.value)
    
    print(f"✅ USDC transfer successful!")
    print(f"   From: {sender_keypair.pubkey()}")
    print(f"   To: {to_address}")
    print(f"   Amount: {amount} USDC")
    print(f"   Signature: {signature}")
    print(f"   Explorer: https://solscan.io/tx/{signature}")
    
    return signature


def main():
    """
    Main entry point for the transfer tool
    """
    parser = argparse.ArgumentParser(
        description="Transfer SOL or USDC tokens on Solana blockchain"
    )
    
    parser.add_argument(
        "token",
        choices=["sol", "usdc", "SOL", "USDC"],
        help="Token type to transfer (sol or usdc)"
    )
    
    parser.add_argument(
        "recipient",
        help="Recipient's Solana address"
    )
    
    parser.add_argument(
        "amount",
        type=float,
        help="Amount to transfer"
    )
    
    args = parser.parse_args()
    
    token_type = args.token.lower()
    
    try:
        if token_type == "sol":
            signature = transfer_sol(args.recipient, args.amount)
        elif token_type == "usdc":
            signature = transfer_usdc(args.recipient, args.amount)
        else:
            print(f"❌ Unsupported token type: {args.token}")
            return 1
        
        print(f"\n🎉 Transfer completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Transfer failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
