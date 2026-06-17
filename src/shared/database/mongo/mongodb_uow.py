from motor.motor_asyncio import AsyncIOMotorClient

class MongoUnitOfWork:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.session = None

    async def __aenter__(self):
        # Khởi tạo session và bắt đầu transaction
        self.session = await self.client.start_session()
        self.session.start_transaction()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                # Nếu không có lỗi, commit các thay đổi
                await self.session.commit_transaction()
            else:
                # Nếu có lỗi (Exception), rollback lại toàn bộ
                await self.session.abort_transaction()
        finally:
            # Luôn kết thúc session
            await self.session.end_session()

    @property
    def get_session(self):
        return self.session

    # Tại đây bạn có thể thêm các Repositories để sử dụng trong UOW
    # ví dụ: 
    # @property
    # def chat_repository(self): return ChatRepository(self.session)