from playwright.async_api import async_playwright


async def check_ip():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(proxy={
                    'server': 'http://207.244.217.165:6712',
                    'username': 'jqsjwunw',
                    'password': 'hd9wm3292a73',
                },
        )
        page = await context.new_page()
        await page.goto('https://api64.ipify.org?format=json')
        ip = await page.inner_text('body')
        print(f'IP: {ip}')
        await browser.close()

import asyncio
asyncio.run(check_ip())
