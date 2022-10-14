# “round-1/Forensics/[Twins](https://github.com/haruulzangi/2022/tree/main/round-1/Forensic/Twins)” даалгаврын writeup

“Twins” буюу ихрүүд гэсэн үгнээс давхардсан агуулгатай файл юм уу мөрийг хайх санаа төрсөн. Давхардсан мөр ганцхан байсан нь: `VU17WkB4M19MMGhlX0dlMGhvIXJfJHZ6YyFsfQ==`.

[base64](https://en.wikipedia.org/wiki/Base64) decode хийвэл: `UM{Z@x3_L0he_Ge0ho!r_$vzc!l}`.

[rot13](https://en.wikipedia.org/wiki/ROT13)-аар хувиргавал: `HZ{M@k3_Y0ur_Tr0ub!e_$imp!y}`. 🎉

Ашигласан script:

```python
import codecs, base64, os

twin, used, root = '', {}, 'FF/'
for path in os.listdir(root):
    for line in open(root + path).readlines():
        if line in used:
            print('1. Found a twin:', line.strip())
            twin = line
        used[line] = True

twin = base64.b64decode(twin).decode()
print('2. Base64 decoded:', twin)

flag = codecs.encode(twin, 'rot13')
print('3. Flag:', flag)

# 1. Found a twin: VU17WkB4M19MMGhlX0dlMGhvIXJfJHZ6YyFsfQ==
# 2. Base64 decoded: UM{Z@x3_L0he_Ge0ho!r_$vzc!l}
# 3. Flag: HZ{M@k3_Y0ur_Tr0ub!e_$imp!y}
```
