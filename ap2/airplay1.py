# SIFTeam OpenAirPlay
# Copyright (C) <2012> skaman (SIFTeam)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
import Crypto
from Crypto.PublicKey import RSA
import base64

import socket


AIRPORT_PRIVATE_KEY = \
    "-----BEGIN RSA PRIVATE KEY-----\n" \
    "MIIEpQIBAAKCAQEA59dE8qLieItsH1WgjrcFRKj6eUWqi+bGLOX1HL3U3GhC/j0Qg90u3sG/1CUt\n" \
    "wC5vOYvfDmFI6oSFXi5ELabWJmT2dKHzBJKa3k9ok+8t9ucRqMd6DZHJ2YCCLlDRKSKv6kDqnw4U\n" \
    "wPdpOMXziC/AMj3Z/lUVX1G7WSHCAWKf1zNS1eLvqr+boEjXuBOitnZ/bDzPHrTOZz0Dew0uowxf\n" \
    "/+sG+NCK3eQJVxqcaJ/vEHKIVd2M+5qL71yJQ+87X6oV3eaYvt3zWZYD6z5vYTcrtij2VZ9Zmni/\n" \
    "UAaHqn9JdsBWLUEpVviYnhimNVvYFZeCXg/IdTQ+x4IRdiXNv5hEewIDAQABAoIBAQDl8Axy9XfW\n" \
    "BLmkzkEiqoSwF0PsmVrPzH9KsnwLGH+QZlvjWd8SWYGN7u1507HvhF5N3drJoVU3O14nDY4TFQAa\n" \
    "LlJ9VM35AApXaLyY1ERrN7u9ALKd2LUwYhM7Km539O4yUFYikE2nIPscEsA5ltpxOgUGCY7b7ez5\n" \
    "NtD6nL1ZKauw7aNXmVAvmJTcuPxWmoktF3gDJKK2wxZuNGcJE0uFQEG4Z3BrWP7yoNuSK3dii2jm\n" \
    "lpPHr0O/KnPQtzI3eguhe0TwUem/eYSdyzMyVx/YpwkzwtYL3sR5k0o9rKQLtvLzfAqdBxBurciz\n" \
    "aaA/L0HIgAmOit1GJA2saMxTVPNhAoGBAPfgv1oeZxgxmotiCcMXFEQEWflzhWYTsXrhUIuz5jFu\n" \
    "a39GLS99ZEErhLdrwj8rDDViRVJ5skOp9zFvlYAHs0xh92ji1E7V/ysnKBfsMrPkk5KSKPrnjndM\n" \
    "oPdevWnVkgJ5jxFuNgxkOLMuG9i53B4yMvDTCRiIPMQ++N2iLDaRAoGBAO9v//mU8eVkQaoANf0Z\n" \
    "oMjW8CN4xwWA2cSEIHkd9AfFkftuv8oyLDCG3ZAf0vrhrrtkrfa7ef+AUb69DNggq4mHQAYBp7L+\n" \
    "k5DKzJrKuO0r+R0YbY9pZD1+/g9dVt91d6LQNepUE/yY2PP5CNoFmjedpLHMOPFdVgqDzDFxU8hL\n" \
    "AoGBANDrr7xAJbqBjHVwIzQ4To9pb4BNeqDndk5Qe7fT3+/H1njGaC0/rXE0Qb7q5ySgnsCb3DvA\n" \
    "cJyRM9SJ7OKlGt0FMSdJD5KG0XPIpAVNwgpXXH5MDJg09KHeh0kXo+QA6viFBi21y340NonnEfdf\n" \
    "54PX4ZGS/Xac1UK+pLkBB+zRAoGAf0AY3H3qKS2lMEI4bzEFoHeK3G895pDaK3TFBVmD7fV0Zhov\n" \
    "17fegFPMwOII8MisYm9ZfT2Z0s5Ro3s5rkt+nvLAdfC/PYPKzTLalpGSwomSNYJcB9HNMlmhkGzc\n" \
    "1JnLYT4iyUyx6pcZBmCd8bD0iwY/FzcgNDaUmbX9+XDvRA0CgYEAkE7pIPlE71qvfJQgoA9em0gI\n" \
    "LAuE4Pu13aKiJnfft7hIjbK+5kyb3TysZvoyDnb3HOKvInK7vXbKuU4ISgxB2bB3HcYzQMGsz1qJ\n" \
    "2gG0N5hvJpzwwhbhXqFKA4zaaSrw622wDniAK5MlIE0tIAKKP4yxNGjoD2QYjhBGuhvkWKY=\n" \
    "-----END RSA PRIVATE KEY-----"


class AP1Security:
    """ Note that some clients will reject the connection: the below algo is correct
    and produces identical results as servers that are accepted. The client just does
    not like something else about how the ap2 receiver is configured. *shrug*

    with request_host = "192.168.128.224"
    with device_id = "48:5D:60:7C:EE:22"
    with apple_challenge "OL/y7hDI1kMrsW8Q7oim4Q"
    must produce "TyNVHs6FPOofPSzOm0iDb3us0UNm4UkwmR4f7fNdaTdL4wolLWsAS7B54ECh26KBvviS1ZUg9eKbou3iRcJCnyoBLa0LNS5xgSRnZgfwER46umZ8nRtTJOc5flyrRt8LFONuc6ZfaW7WA5OeRu6TCj9aXxDqnK6GtGAvKcV002GyHhA+BugRncpIQZU1Q5VVZlwlzR+2acarSuTYCsWDbzy4wohQ8VzgcdW8gJlOpMzr68a7Pxa6X6bhFh5emKB7SusMM1yAca0n2K6kmMkpjFeHoZbg7jRUwn+1A90NAFzLlqb9wxKX7m02xwJYW4RnGuzqzp9CYeak5uuh1T+j0w"

    MessageToCypher : 986236757547332986472011617696226561292849812918563355472727826767720188564083584387121625107510786855734801053524719833194566624465665316622563244215340671405971599343902468620306327831715457360719532421388780770165778156818229863337344187575566725786793391480600129482653072861971002459947277805295727097226389568776499707662505334062639449916265137796823793276300221537201727072401742985542559596685092673521228140822200236743113743661549252453726123450722876929538747702356573783116366629850199080495560991841329893037292397105469608913580097793600298977089331282143331814511067329873718045141765738920411136
    MessageToCypher (hexstr): 0001FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0038BFF2EE10C8D6432BB16F10EE88A6E1C0A880E0485D607CEE22000000000000
    dP : 146709069805088383201933606236299554846046875471360492432859465785731907461821285896560452959452383555075247211256193565876452192906572763346111222064479991426735959971992901274388087191548092712052826625443875992336485040682619774459534956133869295123605378696318067184249309707861838575622021971004870880465
    dQ : 89358255223441375007671327107900674758635355558608906233791412693326780700387446542019888647570870409963774706548328094266078718436492365233599163779035342833912352151811680285184784434465349731078603811225996282706553712976440381351659885853571057111551096934148069500708934951140592911340849534880168494093
    qInv : 101336695669884063581412907835809002361156525909956814201816758827205230154842522398098622230906227512861950039608531447090957492182917970188023197070362861697531742782951776205374512228720067535465611785450234136245601195124085693813856515582829662915588172805381204479537564844263606135608008333455016614054
    M1 : 149172433300423662921496196760335264812991914821074414677090322984242661989244444601222502559141951512882336433807970294415117975874817725123505828843315425085665127400848051106039805892148505480203069235364387827430170399861099583294688582273492370777036383039259083702992626517572518495892582258772557418305
    M2 : 97499814876395269514457077522774393930920370523656157089485413289132480907434203949711967068035644224377880325965099433474841816717797508921561827934667605419264851838660774007529403499574102283518902529932691063870962726325127195096914294893067753044091681426364749663269494159042987965078243546266975566179
    H : 59416704210243383010519657649848967762312539927737895891580525880880708878913385680586502339417457489586388297143842974646233936470309278060829230404522257594789087144274244356081280636772619137477184958934034136253081597139345656624930893013982932533274675769010295633811367869968771311113717903855659440464
    M : 9990249198089170909220682505430267115079044204204110243178803812108984417544935893015471170504250495285989850255914356352755948822920389721418888040569365145544913707276065389205099578605081059802904304178956303720101557716363797562827171272859193554851180868620450908947179657706237114046364815689037844264583783576033155559236330119134011505956018164641274205936032938084397933134470300299688069156553353027041604492875870569989663050823970144760727752775716739696359338356185245049383271613190083337783623194730412896128665706517607698270020470849574923258238066241774542365577017933574080217555232360498716451795
    """
    @staticmethod
    def compute_apple_response(apple_challenge, request_host, device_id):
        # ap2-receiver provides (request_host, device_id) in binary form.
        RSA_KEYLEN = 256

        if apple_challenge[-2:] != "==":
            apple_challenge += "=="
        data = base64.b64decode(apple_challenge)

        # if len(request_host.split(".")) == 4:  # ipv4
        #     data += socket.inet_pton(socket.AF_INET, request_host)
        # elif request_host[:7] == "::ffff:":
        #     data += socket.inet_pton(socket.AF_INET, request_host[7:])
        # else:
        #     data += socket.inet_pton(socket.AF_INET6, request_host.split("%")[0])

        # for i in range(0, 18, 3):
        #     data += bytes.fromhex(device_id[i:i + 2])

        data = data.ljust(32, b"\0")

        message = b"\x00\x01"
        message += b"\xFF" * (RSA_KEYLEN - 32 - 3)
        message += b"\x00"
        message += data
        message += request_host
        message += device_id

        message_bigint = int.from_bytes(message, "big")
        key = RSA.import_key(AIRPORT_PRIVATE_KEY)

        """
        What follows is CRT: Chinese Remainder Theorem. A method for
        more rapidly calculating enrcyption/signature in RSA.
        """
        dP = key.d % (key.p - 1)
        dQ = key.d % (key.q - 1)
        phi = (key.p - 1) * (key.q - 1)
        qInv = modinv(key.q, key.p)
        m1 = pow(message_bigint, dP, key.p)
        m2 = pow(message_bigint, dQ, key.q)
        h = (qInv * (m1 - m2)) % key.p
        m = m2 + h * key.q
        mbin = m.to_bytes(RSA_KEYLEN, byteorder='big')
        m64 = base64.b64encode(mbin)
        if m64[-2:] == b"==":
            m64 = m64[:-2]
        return m64.decode("utf-8")


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


"""
def chineseremaindertheorem(dp, dq, p, q, c):
    # Implementation of the Chinese Remainder Theorem

    # Message part 1
    m1 = pow(c, dp, p)

    # Message part 2
    m2 = pow(c, dq, q)

    qinv = modinv(q, p)

    print(f'qInv: {qinv}')
    print(f'qInv hex: {hex(qinv)}')

    print(f'm1: {m1}')
    print(f'm1 hex: {hex(m1)}')

    print(f'm2: {m2}')
    print(f'm2 hex: {hex(m2)}')
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    print(f'h: {h}')
    print(f'h hex: {hex(h)}')

    print(f'm: {m}')
    print(f'm hex: {hex(m)}')

    return m
"""