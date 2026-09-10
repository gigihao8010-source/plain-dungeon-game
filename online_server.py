import asyncio
import itertools
import math
import time
import os
import websockets

HOST = "0.0.0.0"
PORT = 5050

players = {}
clients = {}
ids = itertools.count(1)
queues = {"1v1": [], "2v2": []}
matches = {}
match_ids = itertools.count(1)
projectile_ids = itertools.count(1)

PVP_MAX_HP = 100
ATTACK_COOLDOWN = 0.45

ARROWS = {
    "regular":   {"damage": 12, "speed": 520, "homing": False, "blast": 0},
    "lightning": {"damage": 14, "speed": 575, "homing": False, "blast": 75},
    "exploding": {"damage": 13, "speed": 470, "homing": False, "blast": 95},
    "homing":    {"damage": 14, "speed": 500, "homing": True,  "blast": 0},
    "fire":      {"damage": 14, "speed": 540, "homing": False, "blast": 0},
    "super":     {"damage": 16, "speed": 590, "homing": True,  "blast": 85},
}

ABILITY_COOLDOWNS = {
    "Knight": {"Z": 4.0, "X": 6.0, "C": 10.0},
    "Ranger": {"Z": 3.0, "X": 4.0, "C": 10.0},
    "Mage":   {"Z": 3.0, "X": 5.0, "C": 9.0},
    "Shadow": {"Z": 3.0, "X": 6.0, "C": 8.0},
}


def adventure_player_message(pid, p):
    return (
        f"PLAYER|{pid}|{p['name']}|{p.get('level',1)}|{p.get('x',110)}|"
        f"{p.get('y',410)}|{p.get('hp',100)}|{p.get('max_hp',100)}|"
        f"{p.get('character','Knight')}|{p.get('facing',1)}|"
        f"{p.get('weapon_mode','sword')}"
    )


def pvp_player_message(pid, p):
    return (
        f"PVPPLAYER|{pid}|{p['name']}|{p.get('team','BLUE')}|"
        f"{p.get('pvp_x',150)}|{p.get('pvp_y',420)}|"
        f"{p.get('pvp_hp',PVP_MAX_HP)}|{p.get('pvp_max_hp',PVP_MAX_HP)}|"
        f"{p.get('character','Knight')}|{p.get('facing',1)}|"
        f"{p.get('weapon_mode','sword')}|{p.get('arrow_type','regular')}"
    )


async def send_to(pid, message):
    websocket = clients.get(pid)
    if websocket is None:
        return
    try:
        await websocket.send(message)
    except Exception:
        pass


async def broadcast(message, skip=None):
    for pid in list(clients):
        if pid != skip:
            await send_to(pid, message)


async def broadcast_match(match_id, message, skip=None):
    match = matches.get(match_id)
    if not match:
        return
    for pid in match["players"]:
        if pid != skip:
            await send_to(pid, message)


async def send_queue_counts():
    await broadcast(f"QUEUECOUNT|1v1|{len(queues['1v1'])}")
    await broadcast(f"QUEUECOUNT|2v2|{len(queues['2v2'])}")


def remove_from_queues(pid):
    for q in queues.values():
        while pid in q:
            q.remove(pid)


def enemy_ids(match_id, attacker_id, living_only=True):
    match = matches.get(match_id)
    attacker = players.get(attacker_id)
    if not match or not attacker:
        return []
    result = []
    for pid in match["players"]:
        if pid == attacker_id:
            continue
        p = players.get(pid)
        if not p or p.get("team") == attacker.get("team"):
            continue
        if living_only and p.get("pvp_hp", 0) <= 0:
            continue
        result.append(pid)
    return result


def nearest_enemy(match_id, attacker_id, max_distance=None):
    attacker = players.get(attacker_id)
    if not attacker:
        return None
    ax = float(attacker.get("pvp_x", 0))
    ay = float(attacker.get("pvp_y", 0))
    best = None
    best_d = 999999
    for pid in enemy_ids(match_id, attacker_id):
        p = players[pid]
        d = math.hypot(float(p.get("pvp_x", 0)) - ax, float(p.get("pvp_y", 0)) - ay)
        if d < best_d and (max_distance is None or d <= max_distance):
            best = pid
            best_d = d
    return best


async def apply_damage(match_id, target_id, damage, effect=None, source=None):
    target = players.get(target_id)
    if not target or target.get("pvp_hp", 0) <= 0:
        return

    now = time.monotonic()
    if target.get("invulnerable_until", 0.0) > now:
        return

    target["pvp_hp"] = max(0, int(target.get("pvp_hp", PVP_MAX_HP) - damage))
    await broadcast_match(
        match_id,
        f"PVPHP|{target_id}|{target['pvp_hp']}|{target.get('pvp_max_hp',PVP_MAX_HP)}"
    )

    if effect:
        tx = float(target.get("pvp_x", 0)) + 20
        ty = float(target.get("pvp_y", 0)) + 35
        sx = tx
        sy = ty
        if source and source in players:
            sx = float(players[source].get("pvp_x", 0)) + 20
            sy = float(players[source].get("pvp_y", 0)) + 35
        await broadcast_match(
            match_id,
            f"PVPEFFECT|{effect}|{sx}|{sy}|{tx}|{ty}|{target.get('team','BLUE')}"
        )

    await finish_match(match_id)


async def try_make_match(mode):
    needed = 2 if mode == "1v1" else 4
    queues[mode] = [
        pid for pid in queues[mode]
        if pid in clients and pid in players and players[pid].get("match_id") is None
    ]
    if len(queues[mode]) < needed:
        await send_queue_counts()
        return

    selected = queues[mode][:needed]
    del queues[mode][:needed]
    match_id = str(next(match_ids))
    teams = ["BLUE", "RED"] if mode == "1v1" else ["BLUE", "BLUE", "RED", "RED"]

    matches[match_id] = {
        "mode": mode,
        "players": selected,
        "over": False,
        "projectiles": {}
    }

    blue_slot = 0
    red_slot = 0

    for pid, team in zip(selected, teams):
        p = players[pid]
        p["match_id"] = match_id
        p["team"] = team
        p["pvp_hp"] = PVP_MAX_HP
        p["pvp_max_hp"] = PVP_MAX_HP
        p["last_attack"] = 0.0
        p["ability_ready"] = {"Z": 0.0, "X": 0.0, "C": 0.0}
        p["berserk_until"] = 0.0
        p["invulnerable_until"] = 0.0
        p["slow_until"] = 0.0
        p["weapon_mode"] = "sword"
        p["arrow_type"] = p.get("arrow_type", "regular")

        if team == "BLUE":
            p["pvp_x"] = 135
            p["pvp_y"] = 385 + blue_slot * 120
            p["facing"] = 1
            blue_slot += 1
        else:
            p["pvp_x"] = 915
            p["pvp_y"] = 385 + red_slot * 120
            p["facing"] = -1
            red_slot += 1

        await send_to(pid, f"MATCH|{mode}|{match_id}|{team}|{PVP_MAX_HP}|{PVP_MAX_HP}")

    for pid in selected:
        for other_id in selected:
            if other_id != pid:
                await send_to(pid, pvp_player_message(other_id, players[other_id]))

    await send_queue_counts()
    print(f"Started {mode} match {match_id}: {selected}")


async def finish_match(match_id):
    match = matches.get(match_id)
    if not match or match["over"]:
        return

    alive_teams = set()
    for pid in match["players"]:
        p = players.get(pid)
        if p and p.get("pvp_hp", 0) > 0:
            alive_teams.add(p.get("team"))

    if len(alive_teams) > 1:
        return

    match["over"] = True
    winner = next(iter(alive_teams), None)
    match["projectiles"].clear()

    for pid in match["players"]:
        p = players.get(pid)
        if not p:
            continue
        result = "WIN" if winner is not None and p.get("team") == winner else "LOSE"
        await send_to(pid, f"RESULT|{result}")
        p["match_id"] = None

    print(f"Match {match_id} finished. Winner: {winner}")


async def spawn_projectile(match_id, owner_id, kind, arrow_type, x, y, vx, vy, damage):
    match = matches.get(match_id)
    owner = players.get(owner_id)
    if not match or not owner:
        return

    proj_id = str(next(projectile_ids))
    match["projectiles"][proj_id] = {
        "id": proj_id,
        "owner": owner_id,
        "team": owner.get("team"),
        "kind": kind,
        "arrow_type": arrow_type,
        "x": float(x),
        "y": float(y),
        "vx": float(vx),
        "vy": float(vy),
        "damage": int(damage),
        "born": time.monotonic()
    }

    await broadcast_match(
        match_id,
        f"PVPPROJ|SPAWN|{proj_id}|{kind}|{arrow_type}|{x}|{y}|{vx}|{vy}|{owner.get('team','BLUE')}"
    )


async def handle_basic_attack(pid, weapon_mode, arrow_type):
    attacker = players.get(pid)
    if not attacker:
        return
    match_id = attacker.get("match_id")
    match = matches.get(match_id)
    if not match or match["over"]:
        return

    now = time.monotonic()
    if now - attacker.get("last_attack", 0.0) < ATTACK_COOLDOWN:
        return
    attacker["last_attack"] = now

    ax = float(attacker.get("pvp_x", 0)) + 20
    ay = float(attacker.get("pvp_y", 0)) + 35
    facing = int(attacker.get("facing", 1))
    multiplier = 1.5 if attacker.get("berserk_until", 0.0) > now else 1.0

    if weapon_mode == "bow":
        arrow_type = arrow_type if arrow_type in ARROWS else "regular"
        attacker["arrow_type"] = arrow_type
        info = ARROWS[arrow_type]
        damage = int(info["damage"] * multiplier)
        speed = info["speed"]
        await spawn_projectile(
            match_id, pid, "ARROW", arrow_type,
            ax + facing * 28, ay,
            facing * speed, 0, damage
        )
        return

    # Sword
    reach = 115
    damage = int(20 * multiplier)
    target_id = None
    best = 999999
    for other_id in enemy_ids(match_id, pid):
        target = players[other_id]
        tx = float(target.get("pvp_x", 0)) + 20
        ty = float(target.get("pvp_y", 0)) + 35
        dx = tx - ax
        dy = ty - ay
        d = math.hypot(dx, dy)
        if dx * facing >= -18 and d <= reach and abs(dy) <= 75 and d < best:
            target_id = other_id
            best = d

    x2 = ax + facing * reach
    y2 = ay
    if target_id:
        x2 = float(players[target_id].get("pvp_x", 0)) + 20
        y2 = float(players[target_id].get("pvp_y", 0)) + 35

    await broadcast_match(match_id, f"PVPEFFECT|SWORD|{ax}|{ay}|{x2}|{y2}|{attacker.get('team','BLUE')}")
    if target_id:
        await apply_damage(match_id, target_id, damage, "HIT", pid)


async def handle_ability(pid, key):
    p = players.get(pid)
    if not p:
        return
    match_id = p.get("match_id")
    match = matches.get(match_id)
    if not match or match["over"]:
        return

    character = p.get("character", "Knight")
    if character not in ABILITY_COOLDOWNS or key not in ("Z", "X", "C"):
        return

    now = time.monotonic()
    ready = p.setdefault("ability_ready", {"Z": 0.0, "X": 0.0, "C": 0.0})
    if now < ready[key]:
        return
    ready[key] = now + ABILITY_COOLDOWNS[character][key]

    x = float(p.get("pvp_x", 0))
    y = float(p.get("pvp_y", 0))
    facing = int(p.get("facing", 1))
    mult = 1.5 if p.get("berserk_until", 0.0) > now else 1.0

    # KNIGHT
    if character == "Knight":
        if key == "Z":  # Shield Rush
            nx = max(55, min(995, x + facing * 160))
            p["pvp_x"] = nx
            await broadcast_match(match_id, f"FORCEPOS|{pid}|{nx}|{y}")
            target = nearest_enemy(match_id, pid, 115)
            if target:
                await apply_damage(match_id, target, int(18 * mult), "HIT", pid)

        elif key == "X":  # Ground Slam
            cx, cy = x + 20, y + 35
            await broadcast_match(match_id, f"PVPEFFECT|SLAM|{cx}|{cy}|{cx}|{cy}|{p.get('team','BLUE')}")
            for target in enemy_ids(match_id, pid):
                t = players[target]
                if math.hypot(float(t.get("pvp_x", 0)) - x, float(t.get("pvp_y", 0)) - y) <= 145:
                    await apply_damage(match_id, target, int(24 * mult), "HIT", pid)

        elif key == "C":  # Berserk
            p["berserk_until"] = now + 5.0
            await broadcast_match(match_id, f"STATUS|{pid}|BERSERK|5000")

    # RANGER
    elif character == "Ranger":
        if key == "Z":  # Triple Shot
            for vy in (-90, 0, 90):
                await spawn_projectile(
                    match_id, pid, "ARROW", p.get("arrow_type", "regular"),
                    x + 20 + facing * 28, y + 35,
                    facing * 550, vy, int(11 * mult)
                )

        elif key == "X":  # Dash
            nx = max(55, min(995, x + facing * 190))
            p["pvp_x"] = nx
            await broadcast_match(match_id, f"FORCEPOS|{pid}|{nx}|{y}")

        elif key == "C":  # Arrow Storm
            for vy in (-220, -145, -75, 0, 75, 145, 220):
                await spawn_projectile(
                    match_id, pid, "ARROW", p.get("arrow_type", "regular"),
                    x + 20 + facing * 28, y + 35,
                    facing * 500, vy, int(9 * mult)
                )

    # MAGE
    elif character == "Mage":
        if key == "Z":  # Fireball
            await spawn_projectile(
                match_id, pid, "FIREBALL", "fire",
                x + 20 + facing * 30, y + 35,
                facing * 430, 0, int(24 * mult)
            )

        elif key == "X":  # Freeze Blast
            target = nearest_enemy(match_id, pid, 235)
            if target:
                players[target]["slow_until"] = now + 2.5
                await broadcast_match(match_id, f"STATUS|{target}|SLOW|2500")
                await apply_damage(match_id, target, int(10 * mult), "HIT", pid)

        elif key == "C":  # Lightning Nova
            cx, cy = x + 20, y + 35
            for target in enemy_ids(match_id, pid):
                t = players[target]
                tx = float(t.get("pvp_x", 0)) + 20
                ty = float(t.get("pvp_y", 0)) + 35
                if math.hypot(tx - cx, ty - cy) <= 190:
                    await broadcast_match(match_id, f"PVPEFFECT|LIGHTNING|{cx}|{cy}|{tx}|{ty}|{p.get('team','BLUE')}")
                    await apply_damage(match_id, target, int(28 * mult), None, pid)

    # SHADOW
    elif character == "Shadow":
        if key == "Z":  # Teleport Strike
            target = nearest_enemy(match_id, pid, 430)
            if target:
                t = players[target]
                tx = float(t.get("pvp_x", 0))
                ty = float(t.get("pvp_y", 0))
                nx = max(55, min(995, tx - facing * 70))
                p["pvp_x"] = nx
                p["pvp_y"] = ty
                await broadcast_match(match_id, f"FORCEPOS|{pid}|{nx}|{ty}")
                await broadcast_match(match_id, f"PVPEFFECT|TELEPORT|{x}|{y}|{nx}|{ty}|{p.get('team','BLUE')}")
                await apply_damage(match_id, target, int(20 * mult), "HIT", pid)

        elif key == "X":  # Vanish
            p["invulnerable_until"] = now + 2.2
            await broadcast_match(match_id, f"STATUS|{pid}|VANISH|2200")

        elif key == "C":  # Spin Attack
            cx, cy = x + 20, y + 35
            await broadcast_match(match_id, f"PVPEFFECT|SPIN|{cx}|{cy}|{cx}|{cy}|{p.get('team','BLUE')}")
            for target in enemy_ids(match_id, pid):
                t = players[target]
                if math.hypot(float(t.get("pvp_x", 0)) - x, float(t.get("pvp_y", 0)) - y) <= 140:
                    await apply_damage(match_id, target, int(23 * mult), "HIT", pid)


async def projectile_loop():
    while True:
        await asyncio.sleep(1 / 30)
        now = time.monotonic()
        dt = 1 / 30

        for match_id, match in list(matches.items()):
            if match.get("over"):
                continue

            for proj_id, proj in list(match.get("projectiles", {}).items()):
                owner_id = proj["owner"]

                # Homing arrows gently turn toward the nearest enemy.
                arrow_info = ARROWS.get(proj["arrow_type"], ARROWS["regular"])
                if proj["kind"] == "ARROW" and arrow_info.get("homing"):
                    target_id = nearest_enemy(match_id, owner_id, 700)
                    if target_id:
                        target = players[target_id]
                        tx = float(target.get("pvp_x", 0)) + 20
                        ty = float(target.get("pvp_y", 0)) + 35
                        dx = tx - proj["x"]
                        dy = ty - proj["y"]
                        d = max(1.0, math.hypot(dx, dy))
                        speed = math.hypot(proj["vx"], proj["vy"])
                        desired_vx = dx / d * speed
                        desired_vy = dy / d * speed
                        proj["vx"] = proj["vx"] * 0.82 + desired_vx * 0.18
                        proj["vy"] = proj["vy"] * 0.82 + desired_vy * 0.18

                proj["x"] += proj["vx"] * dt
                proj["y"] += proj["vy"] * dt

                remove = False
                hit_target = None

                if proj["x"] < 25 or proj["x"] > 1075 or proj["y"] < 190 or proj["y"] > 675:
                    remove = True
                elif now - proj["born"] > 2.5:
                    remove = True
                else:
                    for target_id in enemy_ids(match_id, owner_id):
                        target = players[target_id]
                        tx = float(target.get("pvp_x", 0)) + 20
                        ty = float(target.get("pvp_y", 0)) + 35
                        if math.hypot(tx - proj["x"], ty - proj["y"]) <= 34:
                            hit_target = target_id
                            remove = True
                            break

                if hit_target:
                    await apply_damage(match_id, hit_target, proj["damage"], "HIT", owner_id)

                    # Small special-arrow splash, deliberately PvP-balanced.
                    blast = arrow_info.get("blast", 0)
                    if proj["kind"] == "FIREBALL":
                        blast = 90
                    if blast:
                        for other_id in enemy_ids(match_id, owner_id):
                            if other_id == hit_target:
                                continue
                            t = players[other_id]
                            tx = float(t.get("pvp_x", 0)) + 20
                            ty = float(t.get("pvp_y", 0)) + 35
                            if math.hypot(tx - proj["x"], ty - proj["y"]) <= blast:
                                await apply_damage(match_id, other_id, 5, "HIT", owner_id)

                if remove:
                    match["projectiles"].pop(proj_id, None)
                    await broadcast_match(match_id, f"PVPPROJ|REMOVE|{proj_id}")
                else:
                    await broadcast_match(
                        match_id,
                        f"PVPPROJ|UPDATE|{proj_id}|{proj['x']}|{proj['y']}|{proj['vx']}|{proj['vy']}"
                    )


async def handle_client(websocket):
    pid = str(next(ids))
    name = "Player"
    character = "Knight"

    try:
        first = await websocket.recv()
        parts = str(first).strip().split("|")

        if len(parts) >= 2 and parts[0] == "HELLO":
            name = parts[1][:14] or "Player"
        if len(parts) >= 3 and parts[2] in ("Knight", "Ranger", "Mage", "Shadow"):
            character = parts[2]

        players[pid] = {
            "name": name,
            "level": 1,
            "x": 110,
            "y": 410,
            "hp": 100,
            "max_hp": 100,
            "character": character,
            "facing": 1,
            "weapon_mode": "sword",
            "arrow_type": "regular",
            "match_id": None,
            "team": None
        }
        clients[pid] = websocket

        await websocket.send(f"WELCOME|{pid}")
        print(f"{name} ({character}) connected as player {pid}.")

        async for line in websocket:
            msg = str(line).strip().split("|")
            if not msg:
                continue

            if msg[0] == "STATE" and len(msg) >= 9:
                try:
                    level = int(msg[1])
                    x = float(msg[2])
                    y = float(msg[3])
                    hp = int(float(msg[4]))
                    max_hp = int(float(msg[5]))
                    new_character = msg[6]
                    facing = int(msg[7])
                    weapon_mode = msg[8]
                except ValueError:
                    continue

                p = players[pid]
                p.update(
                    level=max(1, min(5, level)),
                    x=x, y=y,
                    hp=max(0, hp),
                    max_hp=max(1, max_hp),
                    character=new_character if new_character in ("Knight","Ranger","Mage","Shadow") else character,
                    facing=1 if facing >= 0 else -1,
                    weapon_mode=weapon_mode if weapon_mode in ("sword","bow") else "sword"
                )
                await broadcast(adventure_player_message(pid, p), skip=pid)

            elif msg[0] == "QUEUE" and len(msg) >= 2:
                mode = msg[1]
                if mode in queues and players[pid].get("match_id") is None:
                    remove_from_queues(pid)
                    queues[mode].append(pid)
                    await send_queue_counts()
                    await try_make_match(mode)

            elif msg[0] == "LEAVEQUEUE":
                remove_from_queues(pid)
                await send_queue_counts()

            elif msg[0] == "PVPSTATE" and len(msg) >= 7:
                p = players[pid]
                if p.get("match_id") is None:
                    continue
                try:
                    p["pvp_x"] = float(msg[1])
                    p["pvp_y"] = float(msg[2])
                    if msg[3] in ("Knight", "Ranger", "Mage", "Shadow"):
                        p["character"] = msg[3]
                    p["facing"] = 1 if int(msg[4]) >= 0 else -1
                    p["weapon_mode"] = msg[5]
                    if msg[6] in ARROWS:
                        p["arrow_type"] = msg[6]
                except ValueError:
                    continue

                await broadcast_match(p["match_id"], pvp_player_message(pid, p), skip=pid)

            elif msg[0] == "PVPATTACK" and len(msg) >= 2:
                arrow_type = msg[2] if len(msg) >= 3 else players[pid].get("arrow_type", "regular")
                await handle_basic_attack(pid, msg[1], arrow_type)

            elif msg[0] == "PVPABILITY" and len(msg) >= 2:
                await handle_ability(pid, msg[1])

    except Exception as exc:
        print("Client error:", exc)

    finally:
        remove_from_queues(pid)
        p = players.get(pid)
        match_id = p.get("match_id") if p else None

        clients.pop(pid, None)
        players.pop(pid, None)

        if match_id in matches:
            await broadcast_match(match_id, f"PVPLEFT|{pid}", skip=pid)
            await finish_match(match_id)

        await broadcast(f"LEFT|{pid}")
        await send_queue_counts()

        print(f"{name} left.")


async def main():
    port = int(os.environ.get("PORT", PORT))

    async with websockets.serve(
        handle_client,
        HOST,
        port,
        ping_interval=20,
        ping_timeout=20,
        max_size=1024 * 1024
    ):
        asyncio.create_task(projectile_loop())

        print("Sword Adventure ONLINE WebSocket server running!")
        print(f"Port: {port}")
        print("Players can connect from the itch.io browser version.")
        print("Keep this process running while people are playing.")

        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
