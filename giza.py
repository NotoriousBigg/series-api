import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def get_rendered_html(url):
    lua_script = """
    function main(splash)
      splash.private_mode_enabled = false
      splash.images_enabled = false
      assert(splash:go(splash.args.url))
      assert(splash:wait(5))
      return { html = splash:html() }
    end
    """

    async with aiohttp.ClientSession() as session:
        async with session.post("https://splash.kresswell.me/execute", json={
            "url": url,
            "lua_source": lua_script
        }) as resp:
            data = await resp.json()
            return data.get("html")

async def main():
    html = await get_rendered_html("https://videovak.com/en/series/Narcos/S01E01/")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        iframe = soup.find("video")
        if iframe and iframe.has_attr("src"):
            print("Found iframe:", iframe["src"])
        else:
            print("No iframe found.")
    else:
        print("Ni kugumu bois")

if __name__ == '__main__':
    asyncio.run(main())
