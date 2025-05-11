import asyncio
import grpc
from dotenv import load_dotenv
from state_search_be.api import LeanStateSearchServicer
import logging
from state_search_be.state_search.v1.state_search_pb2_grpc import (
    add_LeanStateSearchServiceServicer_to_server,
)
from prisma import Prisma
from qdrant_client import QdrantClient
import os

load_dotenv()

if os.getenv("MODE") == "docker":
    os.environ["DATABASE_URL"] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@pg:5432/statesearch"
    )
else:
    os.environ["DATABASE_URL"] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/statesearch"
    )


async def serve() -> None:
    db = Prisma()
    if os.getenv("MODE") == "docker":
        qdrant_url = "http://qdrant:6333"
        vb = QdrantClient(qdrant_url)
    else:
        # Use local on-disk storage for Qdrant when not in Docker
        qdrant_local_path = "./qdrant_data"
        logging.info(
            f"Using local Qdrant storage at: {os.path.abspath(qdrant_local_path)}"
        )
        vb = QdrantClient(path=qdrant_local_path)
    await db.connect()
    server = grpc.aio.server()
    add_LeanStateSearchServiceServicer_to_server(
        LeanStateSearchServicer(db=db, vb=vb), server
    )

    listen_addr = f"[::]:{os.getenv('BACKEND_PORT')}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()
    await server.wait_for_termination()
    await db.disconnect()


def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())


if __name__ == "__main__":
    main()
