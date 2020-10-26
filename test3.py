import asyncio


class X:
    def __init__(self):
        self.qq = asyncio.Queue()
    async def work(self, sem, qq):
        async with sem:
            print(qq.empty())
            while qq.empty():
                await asyncio.sleep(1)
                print(1)
            print('working')
            await asyncio.sleep(1)


    async def main(self, qq):
        sem = asyncio.Semaphore(1)
        await asyncio.gather(work(sem, qq))



asyncio.run(main(qq))
qq.put(1)