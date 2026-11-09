import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup


class Parser:
    def __init__(self,collection,model):
        self.collection = collection
        self.model = model
        self.nfts = []

    async def __get_info(self,number,session):
        async with  session.get(f'https://t.me/nft/{self.collection}-{number!s}') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            meta_tag = soup.find('meta', property="og:description")
            description = meta_tag.get('content', '') if meta_tag else ''

            self.nfts.append(description)
            return description

    async def __get_amount(self,session):
        async with session.get(f'https://t.me/nft/{self.collection}-1') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            text = soup.text.replace('\n', '')
            arr = list(text[text.find('Quantity'):text.find('/')].replace('Quantity', ''))
            if len(arr) > 3:
                arr.pop(-4)



            num_str = ''.join(arr).strip()

            if num_str:
                supply = int(num_str)
            else:
                supply = 0



            return  supply

    async def main(self):
        async with aiohttp.ClientSession() as session:
            start = time.time()
            supply = await self.__get_amount(session)
            tasks = [asyncio.create_task(self.__get_info(i,session)) for i in range(1,supply)]
            await asyncio.gather(*tasks)

            for nft in self.nfts:
                print(nft)

            print(time.time() - start)


    def run(self):
        asyncio.run(self.main())

if __name__ == "__main__":
    gem_signet = Parser("GemSignet", "Feral Rage")
    gem_signet.run()
