import asyncio, sys
from playwright.async_api import async_playwright

URL = "http://localhost:8765/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 820, "height": 900}, device_scale_factor=1)
        erros = []
        pg.on("console", lambda m: erros.append(m.text) if m.type == "error" and "fonts" not in m.text and "ERR_" not in m.text else None)
        pg.on("pageerror", lambda e: erros.append("PAGEERROR " + str(e)))
        await pg.goto(URL, wait_until="domcontentloaded")
        await pg.wait_for_selector("#palco .cena")
        passos = 0; shots = {}
        vistos = set()
        while passos < 300:
            passos += 1
            await pg.wait_for_timeout(10); print("passo", passos, flush=True) if passos % 25 == 0 else None
            html = await pg.inner_html("#palco")
            # espelho
            if "Quem é você" in html:
                for _ in range(3):
                    await pg.click("[data-mais='forca']")
                await pg.screenshot(path="/tmp/shots/espelho.png")
                await pg.click(".confirmar"); continue
            if "Escolha 2 virtudes" in html:
                bts = await pg.query_selector_all("[data-id]")
                await bts[0].click(); 
                bts = await pg.query_selector_all("[data-id]"); await bts[2].click()
                await pg.screenshot(path="/tmp/shots/virtudes.png")
                await pg.click(".confirmar"); continue
            if "Perfeito demais" in html:
                await pg.click("#btn-avancar-tracos"); continue
            if "Escolha 1 vício" in html:
                bts = await pg.query_selector_all("[data-id]"); await bts[1].click()
                await pg.click(".confirmar"); continue
            if await pg.query_selector("#btn-avancar"):
                await pg.click("#btn-avancar"); continue
            if await pg.query_selector("#btn-seguir"):
                await pg.click("#btn-seguir"); continue
            esc = await pg.query_selector_all(".escolha")
            if esc:
                txt = (await esc[0].inner_text()).strip()
                if "recomeçar" in txt:
                    await pg.screenshot(path="/tmp/shots/fim.png"); break
                await esc[0].click(); continue
            await pg.wait_for_timeout(200)
        # estado final
        topo = await pg.inner_text("#status")
        print("passos:", passos); print("topo:", topo.replace("\n", " | "))
        # painéis
        for nome in ["perfil", "social", "inventario"]:
            await pg.click("#btn-" + nome); await pg.wait_for_timeout(100)
            await pg.screenshot(path=f"/tmp/shots/painel_{nome}.png")
            print(nome, "->", (await pg.inner_text("#painel")).replace("\n", " | ")[:260])
        await pg.click("#btn-mapa"); await pg.wait_for_timeout(100)
        await pg.screenshot(path="/tmp/shots/painel_mapa.png")
        print("mapa ->", (await pg.inner_text("#painel")).replace("\n", " | ")[:300])
        print("erros de console:", erros or "nenhum")
        await b.close()
asyncio.run(main())
