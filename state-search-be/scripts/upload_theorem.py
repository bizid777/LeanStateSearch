from prisma import Prisma
import jsonlines
import argparse
import asyncio
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["DATABASE_URL"] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/statesearch"
)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--rev", type=str, required=True)

    args = parser.parse_args()
    db = Prisma()
    theorems = []
    await db.connect()
    with jsonlines.open(args.data_path, "r") as f:
        for it in tqdm(f.iter()):  # type: ignore[assignment]
            data: dict = dict(it)  # type: ignore[arg-type]
            theorems.append({
                "name": data["full_name"],
                "args": data["args"],
                "goal": data["goal"],
                "module": data["mod_name"],
                "rev": args.rev,
            })
    await db.theorem.create_many(data=theorems)
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
