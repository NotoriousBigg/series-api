from bs4 import BeautifulSoup
from httpx import AsyncClient
from fastapi import HTTPException
import asyncio
async def get_soup(url):
    async with AsyncClient(timeout=30) as xx:
        res = await xx.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            return soup
        return None

async def get_series_data(series_id):
    try:
        soup = await get_soup(f"https://videovak.com/en/series/{series_id}/")
        if not soup:
            raise HTTPException(
                status_code=403,
                detail="Invalid series id"
            )


        title = soup.find('div', attrs={"class": "DescTitle"}).text.strip()
        tags = soup.find("div", attrs={"class": "DescGenre"}).text.strip()
        description = soup.find("div", attrs={"class": "Description"}).text.strip()
        tgs = []
        for tag in tags.split(" - "):
            tgs.append(tag)

        seasons =  soup.find_all("div", attrs={"class": "SeasonBlock"})
        seasons = len(seasons)


        episodes_list = soup.find("div", attrs={"class": "EpisodeContainer"})
        eps = []
        for episode in episodes_list.find_all("div", attrs={"class": "EpisodeBlock"}):
            imdb_id = episode.find("div", attrs={'class': 'EpisodeIMDB'}).text.strip()
            ep_number = episode.find("div", attrs={'class': 'EpisodeNumber'}).text.strip()
            eps.append({
                "imdb_rating": imdb_id,
                "episode_number": ep_number
            })
        combo = {
            "title": title,
            "tags": tgs,
            "description": description,
            "episodes": eps,
            "seasons": seasons
        }
        print(combo)

    except Exception as y:
        raise HTTPException(
            detail=y,
            status_code=500
        )


async def main():
    soup = await get_soup("https://videovak.com/en/series/Narcos/S01E01/")
    if soup:
        video_tag = soup.find("video")
        source = video_tag
        print(video_tag)
    else:
        print("Ni kugumu bois")

if __name__ == '__main__':
    asyncio.run(main())