# gọi 10 URL tuần tự, rồi song song bằng gather, rồi giới hạn đồng thời bằng Semaphore.
# tìm api free trên mạng để test, ví dụ: https://jsonplaceholder.typicode.com/posts/1
#so sánh thời gian thực hiện 3 cách trên, in ra kết quả và thời gian thực hiện.

import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_sequential(urls):
    async with aiohttp.ClientSession() as session:
        time_start = asyncio.get_event_loop().time()
        results = []
        for url in urls:
            result = await fetch(session, url)
            results.append(result)
        time_end = asyncio.get_event_loop().time()
        print(f"Sequential time: {time_end - time_start}")
        return results

async def fetch_concurrent(urls):
    async with aiohttp.ClientSession() as session:
        time_start = asyncio.get_event_loop().time()
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        time_end = asyncio.get_event_loop().time()
        print(f"Concurrent time: {time_end - time_start}")
        return results

async def fetch_limited(urls, limit):
    semaphore = asyncio.Semaphore(limit)
    async with aiohttp.ClientSession() as session:
        time_start = asyncio.get_event_loop().time()
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await fetch(session, url)
        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks)
        time_end = asyncio.get_event_loop().time()
        print(f"Limited time: {time_end - time_start}")
        return results

async def main():
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]

    print("Fetching sequentially...")
    await fetch_sequential(urls)

    print("Fetching concurrently...")
    await fetch_concurrent(urls)

    print("Fetching with limited concurrency (limit=3)...")
    await fetch_limited(urls, limit=3)

if __name__ == "__main__":
    asyncio.run(main())