from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Listing
from .schemas import ListingCreate, ListingResponse, ListingUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Avito API",
    description="Учебный REST API доски объявлений с полным CRUD.",
    version="1.0.0",
)


@app.get("/", tags=["Сервис"])
def root() -> dict[str, str]:
    return {"message": "Avito API работает", "docs": "/docs"}


@app.post("/listings", response_model=ListingResponse, status_code=status.HTTP_201_CREATED, tags=["Объявления"])
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)) -> Listing:
    listing = Listing(**payload.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@app.get("/listings", response_model=list[ListingResponse], tags=["Объявления"])
def read_listings(
    category: str | None = Query(None, description="Фильтр по категории"),
    city: str | None = Query(None, description="Фильтр по городу"),
    search: str | None = Query(None, description="Поиск по названию"),
    db: Session = Depends(get_db),
) -> list[Listing]:
    query = select(Listing).order_by(Listing.created_at.desc())
    if category:
        query = query.where(Listing.category == category)
    if city:
        query = query.where(Listing.city == city)
    if search:
        query = query.where(Listing.title.ilike(f"%{search}%"))
    return list(db.scalars(query).all())


@app.get("/listings/{listing_id}", response_model=ListingResponse, tags=["Объявления"])
def read_listing(listing_id: int, db: Session = Depends(get_db)) -> Listing:
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return listing


@app.patch("/listings/{listing_id}", response_model=ListingResponse, tags=["Объявления"])
def update_listing(listing_id: int, payload: ListingUpdate, db: Session = Depends(get_db)) -> Listing:
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)
    db.commit()
    db.refresh(listing)
    return listing


@app.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Объявления"])
def delete_listing(listing_id: int, db: Session = Depends(get_db)) -> Response:
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    db.delete(listing)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
