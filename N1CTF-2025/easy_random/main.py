from os import close
from pwn import *
import datetime
import hashlib, itertools, string, hmac

context.terminal = [
    "zellij",
    "action",
    "new-pane",
    "-f",
    "-c",
    "--",
    "bash",
    "-c",
]

TEAM = b"WE_0WN_Y0U"
PASSWORD = b"admin"


def init():
    if args.LOCAL:
        p = process("./easy_random_demo")
    else:
        p = remote("60.205.163.215", 33935)
    return p


def pow(tail: bytes, target_hex: str, full=False, charset=None):
    target = bytes.fromhex(target_hex)
    if len(target) != 16:
        raise ValueError("target must be 16 bytes (32 hex chars)")
    if full:
        gen = (
            bytes((a, b, c)) for a in range(256) for b in range(256) for c in range(256)
        )
    else:
        chars = (
            charset if charset is not None else (string.ascii_letters + string.digits)
        )
        cb = [c.encode() for c in chars]
        gen = (a + b + c for a, b, c in itertools.product(cb, repeat=3))
    for p in gen:
        if hashlib.md5(p + tail).digest()[:16] == target:
            return p
    return None


def totp(key: bytes, counter: int, digits: int = 6) -> int:
    """
    Compute the TOTP code for `key` at `counter` (time//30).
    """
    # 8-byte big-endian counter
    msg = struct.pack(">Q", counter)

    # HMAC-SHA1 of key and counter
    digest = hmac.new(key, msg, hashlib.sha1).digest()

    # dynamic truncation: last byte & 0x0F
    offset = digest[-1] & 0x0F

    # get 4 bytes starting at offset, mask top bit
    code_int = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF

    return code_int % (10**digits)


def calculate_otp(p, time):
    time //= 30
    time += 120

    if args.LOCAL:
        otp = p.recvline().decode().strip().split(": ")[-1]
    else:
        otp = totp(TEAM, time)

    return str(otp)


def login(p):
    p.recvuntil(b"Current time: ")
    time_string = p.recvline().strip().decode()[:-1]
    dt = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    time_int = int(dt.timestamp())

    p.recvuntil(b"): ")  # username
    p.sendline(TEAM)
    p.recvuntil(b":")  # password
    p.sendline(PASSWORD)
    otp = calculate_otp(p, time_int)
    p.sendlineafter(b"code:", str(otp).encode())


def solve_pow(p):
    p.recvuntil(b"Pow:")
    p.recvline()
    data = p.recvline().strip()
    tail, target_hex = data.split(b":")
    info("Solving PoW...")
    info(f"tail: {tail}, target: {target_hex}")
    prefix = pow(tail, target_hex.decode())
    info(f"Found prefix: {prefix}")
    p.sendline(prefix)


def solve_level_one(p):
    pts = 0
    for i in range(10):
        import random

        random_bit = random.randint(0, 1)
        guess = b"H" if random_bit == 1 else b"T"
        p.recvuntil(b"guess:")
        import random

        random_bit = random.randint(0, 1)
        guess = b"H" if random_bit == 1 else b"T"
        p.sendline(guess)
        line = (p.recvline().decode().strip()).split()
        pts_gained = int(line[-2])
        info(f"Round {i}: guessed {guess.decode()}, points gained: {pts_gained}")
        if pts_gained == 0 and not args.LOCAL:
            p.close()
            solve()
        pts += pts_gained

    info(f"Total points: {pts}")
    if pts >= 10:
        info("Level one solved!")
        return
    else:
        p.close()
        solve()


def solve_level_two(p):
    groups = []
    p.recvuntil(b"missing coins.\n")
    for i in range(16):
        data = p.recvline().decode().strip().split(": ")[-1]
        data = data.split()
        data = ["H" if x == "Head" else "T" for x in data]
        p.sendline(b"OK!")
        groups.append(data)

    for i in range(16):
        info(f"Group {i}: {groups[i]}")

    for i in range(16):
        data = p.recvline().decode()

        if "Error" in data:
            warn(data)
            p.close()
            solve()

        data = data.strip().split(": ")[-1]
        data = data.split()
        group = ["H" if x == "Head" else "T" for x in data]

        info(f"Analyzing group: {group}")

        count_H = group.count("H")
        count_T = group.count("T")

        possible_groups = []
        for j in range(16):
            g = groups[j]
            if (g.count("H") == count_H + 1 and g.count("T") == count_T) or (
                g.count("H") == count_H and g.count("T") == count_T + 1
            ):
                possible_groups.append((j, g))

        found = False
        missing_coing = "X"
        for idx, g in possible_groups:
            for k in range(6):
                if g[k] != group[k]:
                    missing_coing = "H" if g[k] == "H" else "T"
                    
                    new = group[:k]
                    new.append(missing_coing)
                    new += group[k:]

                    info(f"Identified missing coin in group {idx}, position {k}")
                    info(f"Missing coin is: {missing_coing}")
                    info(f"Resulting array: {new}")
                    
                    missmatch = 0

                    for l in range(6):
                        if g[k] != new[l]:
                            missmatch += 1                  

                    info(f"Missmatches: {missmatch}")

                    if missmatch > 3:
                        break

                    info(possible_groups)
                    p.recvuntil(b"You guess:")
                    p.sendline(missing_coing)

                    found = True
                    break

            if found:
                break

        if found == False:
            warn("No match found")
            p.close()
            solve()


def solve():
    p = init()
    login(p)
    solve_pow(p)
    solve_level_one(p)
    solve_level_two(p)

    info("Back to interactive!")
    p.interactive()


solve()
