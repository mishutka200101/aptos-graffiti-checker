import asyncio
from aiohttp import ClientSession


def read_wallets():
    with open("wallets.txt", "r") as file:
        wallets = file.read().split("\n")
        wallets = [wallet.strip() for wallet in wallets]

    return wallets


def parse_transactions(txs: list) -> int:
    counter = 0

    for tx in txs:
        try:
            if tx["payload"]["function"] == "0x915efe6647e0440f927d46e39bcb5eb040a7e567e1756e002073bc6e26f2cd23::canvas_token::draw":
                counter += 1
        except Exception:
            pass

    return counter


async def get_transactions(session: ClientSession, wallet_address: str):
    params = {
        "sender": f"eq.{wallet_address}",
        "limit": "50",
    }
    async with session.get("https://api.apscan.io/user_transactions", params=params) as res:
        try:
            return await res.json()
        except Exception:
            return []


async def run_all(wallets: list) -> list:
    async with ClientSession(headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}) as session:
        tasks = [get_transactions(
            session=session, wallet_address=wallet) for wallet in wallets]
        return await asyncio.gather(*tasks)


def main():
    wallets = read_wallets()
    result = asyncio.run(run_all(wallets=wallets))

    itog = []

    for i, res in enumerate(result):
        itog.append([wallets[i], parse_transactions(txs=res)])

    with open("result.txt", "w") as file:
        file.write("address;graffiti_txs\n")
        for item in itog:
            file.write(f"{item[0]};{item[1]}\n")


if __name__ == "__main__":
    print("Обработка начата...")
    main()
    print("Результат сохранен в файл 'result.txt'\nМожно импортировать его в Excel, разделитель ;")
