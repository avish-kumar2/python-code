moi_mov = [-1001387857902]

async def apd_scheduler():
    mobies = udB.hgetall("AUTO_MOVIE")
    for chnnl, ids in mobies.items():
        chnnl = int(chnnl) if str(chnnl).isdigit() else str(chnnl)
        lasty = (await ultroid.get_messages(chnnl, limit=1))[0]
        if int(ids) == lasty.id:
            LOGS.info(f"••• Everything Backed-up from ~ {chnnl}")
            continue

        tt1, cnt = time.time(), 0
        async for x1 in ultroid.iter_messages(
            chnnl, min_id=int(ids), reverse=True,
        ):
            udB.hset("AUTO_MOVIE", chnnl, str(x1.id))
            await asyncio.sleep(1)
            if x1 and x1.video:
                try:
                    await ultroid.send_file(ENTX, x1, caption=x1.text, silent=True)
                    cnt += 1
                    await asyncio.sleep(randrange(5, 16))
                except FloodWaitError as ex:
                    await asyncio.sleep(ex.seconds + 30)
                except Exception as ex:
                    LOGS.error(f"\n\n••• Error Movie fwd SCHD: \n{ex}\n")

        LOGS.info(f"\n\n••• Copied {cnt} movies from ~ {chnnl}! | " \
            f"Time taken ~ {round(time.time() - tt1)}s \n")

schedule.add_job(apd_scheduler, "interval", minutes=35, id="apd_schd")