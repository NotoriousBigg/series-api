from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from httpx import AsyncClient

app = FastAPI(
    title="videovak api",
    description="A free api for interacting with videovak.com to retrieve series data",
    docs_url="/"
)

# Utility function to get BeautifulSoup object from URL
async def get_soup(url):
    async with AsyncClient(timeout=30) as client:
        res = await client.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            return soup
        return None

# Route: Series details
@app.get("/series/{series_id}")
async def get_series_data(series_id: str):
    try:
        soup = await get_soup(f"https://videovak.com/en/series/{series_id}/")
        if not soup:
            raise HTTPException(status_code=403, detail="Invalid series id")

        title = soup.find('div', class_="DescTitle").text.strip()
        tags = soup.find("div", class_="DescGenre").text.strip()
        description = soup.find("div", class_="Description").text.strip()
        tgs = [tag.strip() for tag in tags.split(" - ")]

        seasons = soup.find_all("div", class_="SeasonBlock")
        seasons_count = len(seasons)

        episodes_list = soup.find("div", class_="EpisodeContainer")
        eps = []
        for episode in episodes_list.find_all("div", class_="EpisodeBlock"):
            imdb_id = episode.find("div", class_="EpisodeIMDB").text.strip()
            ep_number = episode.find("div", class_="EpisodeNumber").text.strip()
            eps.append({
                "imdb_rating": imdb_id,
                "episode_number": ep_number
            })

        return JSONResponse(
            content={
                "title": title,
                "tags": tgs,
                "description": description,
                "episodes": eps,
                "seasons": seasons_count
            },
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Episode details
@app.get("/series/{series}/season/{season}/episode/{episode}")
async def get_episode_data(series: str, season: str, episode: str):
    try:
        url = f"https://videovak.com/en/series/{series}/S{season}E{episode}/"
        soup = await get_soup(url)
        if not soup:
            raise HTTPException(status_code=403, detail="Invalid episode or series")

        video_tag = soup.find("div", class_="EpisodeInfoContainer")
        torrent = video_tag.find("a").get("href") if video_tag and video_tag.find("a") else None
        ep_title = soup.find("div", class_="EpisodeTitle").text.strip()
        ep_description = soup.find("div", class_="EpisodeDesc").text.strip()

        return JSONResponse(
            content={
                "title": ep_title,
                "description": ep_description,
                "source": torrent # most of the torrents aer dead as they no longer have seeders.
            },
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
