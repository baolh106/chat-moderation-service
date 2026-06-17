import os
import urllib.parse
from dataclasses import dataclass

@dataclass
class MongoDBConfig:
    protocol: str
    cluster: str
    db_name: str
    username: str
    password: str
    retry_writes: bool = True
    write_concern: str = "majority"

    @property
    def connection_uri(self) -> str:
        if self.cluster.startswith("mongodb://") or self.cluster.startswith("mongodb+srv://"):
            return self.cluster

        auth = ""
        if self.username and self.password:
            user = urllib.parse.quote_plus(self.username)
            pwd = urllib.parse.quote_plus(self.password)
            auth = f"{user}:{pwd}@"

        base_uri = f"{self.protocol}://{auth}{self.cluster}/{self.db_name}"
        params = f"retryWrites={'true' if self.retry_writes else 'false'}&w={self.write_concern}"
        return f"{base_uri}?{params}"

mongo_config = MongoDBConfig(
    protocol=os.getenv("MONGO_PROTOCOL", "mongodb"),
    cluster=os.getenv("MONGO_CLUSTER", "localhost:27017"),
    db_name=os.getenv("MONGO_DB_NAME", "chat_moderation"),
    username=os.getenv("MONGO_USERNAME", ""),
    password=os.getenv("MONGO_PASSWORD", ""),
)