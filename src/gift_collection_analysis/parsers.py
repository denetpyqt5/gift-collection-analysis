import asyncio
import time
import random

import aiohttp
from bs4 import BeautifulSoup


class Parser:
    def __init__(self,collection):
        self.collection = collection
        self.__nfts = {}

    async def __get_info(self,number,session,sem):
        async with  session.get(f'https://t.me/nft/{self.collection}-{number!s}') as response:
            async with sem:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                meta_tag = soup.find('meta', property="og:description")
                description = meta_tag.get('content', '') if meta_tag else ''
                await asyncio.sleep(random.randint(1,5))
                self.__nfts[number.__str__()] = description
                return description

    async def __get_amount(self,session):
        async with session.get(f'https://t.me/nft/{self.collection}-1') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            text = soup.text.replace('\n', '')
            arr = list(text[text.find('Quantity'):text.find('/')].replace('Quantity', ''))
            if len(arr) > 3:
                arr.pop(-4)
            num_str = ''.join(arr).strip()
            supply = int(num_str) if num_str else 0
            return  supply

    async def main(self):
        async with aiohttp.ClientSession() as session:
            supply = await self.__get_amount(session)
            sem = asyncio.Semaphore(3)
            tasks = [asyncio.create_task(self.__get_info(i,session,sem)) for i in range(1,supply)]
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.main())

        for number,nft in self.__nfts.items():
            print(number, nft)