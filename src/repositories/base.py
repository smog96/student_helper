from sqlalchemy import func, select
from pydantic import BaseModel
from src.db.session import get_sync_db
from src.shared.decorators import no_result


class BaseRepository:
    def __init__(self):
        self.db = get_sync_db()

    def fetch_total(self, query) -> int:
        query = (
            query.select_from(self.model)
            .with_only_columns(func.count(self.model.id).label("total"))
            .group_by(None)
            .order_by(None)
            .limit(None)
            .offset(None)
        )
        result = self.db.execute(query)
        total = result.fetchone()
        return total["total"] if total is not None else 0

    @no_result(True)
    def return_scalars_(self, query, is_unique: bool = False):
        result = self.db.execute(query)
        if is_unique:
            return result.unique().scalars().all()
        return result.scalars().all()

    @no_result()
    def return_scalar_(self, query, is_unique: bool = False):
        result = self.db.execute(query)
        if is_unique:
            return result.unique().scalar()
        return result.scalar()

    @no_result()
    def return_scalar_one_(self, query, is_unique: bool = False):
        print(query)
        result = self.db.execute(query)
        if is_unique:
            return result.unique().scalar_one()
        return result.scalar_one()

    def add(self, item: BaseModel):
        db_item = self.model(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get(self, id_: int = None, **filters):
        query = select(self.Model)

        if id_:
            query = query.where(self.model.id == id_)

        for k, v in filters.items():
            if k not in [
                "is_unique",
            ]:
                query = query.where(k == v)
        return self.return_scalars_(query, is_unique=filters.get("is_unique", False))

    @property
    def model(self):
        raise NotImplementedError
