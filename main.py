from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from web3 import Web3

# Step 0: Load the bot token and Ethereum connection
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
INFURA_API_KEY: Final[str] = os.getenv('INFURA_API_KEY')
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_API_KEY}'))

# Replace 'YOUR_CONTRACT_ADDRESS' with the actual contract address
contract_address = '0x24d667C5195a767819C9313D6ceEC09D0Dc06Cfd'

# Replace 'YOUR_CONTRACT_ABI' with the actual contract ABI
contract_abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [], "name": "AccessControlBadConfirmation", "type": "error"},
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"},
                {"internalType": "bytes32", "name": "neededRole", "type": "bytes32"}],
     "name": "AccessControlUnauthorizedAccount", "type": "error"},
    {"inputs": [], "name": "EnforcedPause", "type": "error"},
    {"inputs": [], "name": "ExpectedPause", "type": "error"},
    {"inputs": [], "name": "ReentrancyGuardReentrantCall", "type": "error"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}],
     "name": "Paused", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"},
                                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}],
     "name": "PointsAdded", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"},
                                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}],
     "name": "PointsRemoved", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}],
     "name": "PointsTransferred", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"indexed": True, "internalType": "bytes32", "name": "previousAdminRole", "type": "bytes32"},
                {"indexed": True, "internalType": "bytes32", "name": "newAdminRole", "type": "bytes32"}],
     "name": "RoleAdminChanged", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"indexed": True, "internalType": "address", "name": "account", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "sender", "type": "address"}],
     "name": "RoleGranted", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"indexed": True, "internalType": "address", "name": "account", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "sender", "type": "address"}],
     "name": "RoleRevoked", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}],
     "name": "Unpaused", "type": "event"},
    {"inputs": [], "name": "DEFAULT_ADMIN_ROLE", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "POINTS_MANAGER_ROLE", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"}],
     "name": "addPoints", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "newMultiplier", "type": "uint256"}], "name": "changeMultiplier",
     "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "user", "type": "address"}], "name": "drainPoints", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}], "name": "getRoleAdmin", "outputs": [
        {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "manager", "type": "address"}], "name": "grantManager", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"}], "name": "grantRole", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"}], "name": "hasRole", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "multiplier", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "paused", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}],
     "name": "points", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "removePoints", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "callerConfirmation", "type": "address"}], "name": "renounceRole",
     "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "manager", "type": "address"}], "name": "revokeManager", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"}], "name": "revokeRole", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface",
     "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferPoints", "outputs": [],
     "stateMutability": "nonpayable", "type": "function"}
]


# Create a contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Step 1: Bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Step 2: Message functionality
async def send_message(message: Message, response: str) -> None:
    if not response:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    try:
        await message.channel.send(response)
    except Exception as e:
        print(e)

# Step 3: Handling the startup for our bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Step 4: Handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    # Check if the message starts with "/"
    if user_message.startswith('/'):
        # Extract the wallet address from the message
        wallet_address = user_message[1:]

        try:
            # Call the 'points' function of the contract
            points = contract.functions.points(wallet_address).call()

            # Send the points as a response
            response = f"{points} Phunky Points"
            await send_message(message, response)
        except Exception as e:
            print(e)
            
    else:
        return

# Step 5: Main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()