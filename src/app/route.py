from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
import jwt
from jose import JWTError

from src.app.schema import UrlGettter
from src.app.service import get_short_url
from src.DB.main import get_session
from src.DB.model import UrlMapper
from src.config.config import Config

from sqlmodel import select

app_route = APIRouter()
security = HTTPBearer()


@app_route.get("/")
async def landing_page(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        return {"payload":payload, "message" : "Hi welcome to our URL shortner service"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

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
    if url_record is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url_record.num_visits += 1
    session.add(url_record)
    session.commit()
    return RedirectResponse(url=url_record.url)



