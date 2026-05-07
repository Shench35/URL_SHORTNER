from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from src.app.schema import UrlGettter
from src.app.service import get_short_url
from src.DB.main import get_session
from src.DB.model import UrlMapper

from sqlmodel import select, update

app_route = APIRouter()


@app_route.get("/")
async def landing_page():
    return {"message" : "Hi welcome to our URL shortner service"}

@app_route.post("/get_url")
def get_url(url:UrlGettter, session = Depends(get_session)):
    url_data = url.model_dump()
    short_url = get_short_url()

    statement = select(UrlMapper).where(UrlMapper.shortened_url==short_url)
    exist = session.exec(statement).first()

    while exist:
        short_url = f"shorter/{get_short_url()}"
        statement = select(UrlMapper).where(UrlMapper.shortened_url==short_url)
        exist = session.exec(statement).first()

    db_data = UrlMapper(
        title=url_data.get("title"),
        url=url_data.get("url"),
        shortened_url=short_url,
        num_visits=0
    )
    
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    
    return {"shortened_url": short_url, "original_url": url_data.get("url")}

@app_route.get("/{short_url}")
def redirect_shortened_url(short_url:str, session=Depends(get_session)):
    statement = select(UrlMapper).where(UrlMapper.shortened_url==short_url)
    url_record = session.exec(statement).one_or_none()
    print(type(url_record))
    if url_record:
        url_record.num_visits += 1
        session.add(url_record)
        session.commit()
    return RedirectResponse(url=url_record.url)
    return {"error": "Short URL not found"}



