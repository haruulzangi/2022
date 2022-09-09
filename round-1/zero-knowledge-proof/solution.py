from pwn import *
import random

g = 3

# context.log_level = 'debug'

conn = remote('localhost', 1337)
conn.recvuntil(b'p: ')
p = int(conn.recvline())
log.debug('p:', p)

x = random.randint(2, p - 1)
y = pow(g, x, p)
conn.sendlineafter(b'Give me your y: ', str(y).encode('ascii'))

with log.progress('Solving challenge') as progress:
	for i in range(256):
		progress.status(f'Round {i}')
		r = random.randint(2, p - 2)
		C = pow(g, r, p)
		conn.sendlineafter(b'Send me value of C: ', str(C).encode('ascii'))

		challenge_type = 'A' if b'A' in conn.recvuntil(b'solution:') else 'B'
		if challenge_type == 'A':
			conn.sendline(str(r).encode('ascii'))
		else:
			conn.sendline(str((x + r) % (p - 1)).encode('ascii'))

log.success(conn.recvall().decode('ascii').strip())
conn.close()
