package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"math/big"
	"net"
	"os"
)

const (
	greeting = `Hello there! My name is Victor and I'm a verifier for this challenge.

How to play:
1. Take a number p, which is a large prime
2. Generate some random number x
3. Compute y = g^x mod p (g = 3)

Then the real game starts! There are 64 rounds in total, so please make sure to automate everything :)
For each round:
1. Generate some random number 0 < r < p - 1
2. Compute C = g^r mod p and send it to me
3. Send solution for a problem sent by me
4. Proceed to the next round

There are two kinds of problems: A and B.
Problem A: send r
Problem B: compute value of (x + r) mod (p - 1)

For more information: https://en.wikipedia.org/wiki/Zero-knowledge_proof#Discrete_log_of_a_given_value
`
	totalRounds = 64
)

var (
	p    *big.Int
	g    = big.NewInt(3)
	flag = "HZ{Z3r0_kn0wl3dg3_pr00F_is_f1t1r3_OYfFd8ZQEUWj2}"
)

func session(conn net.Conn) {
	defer conn.Close()

	_, err := conn.Write([]byte(greeting))
	if err != nil {
		return
	}

	_, err = conn.Write([]byte(fmt.Sprintf("\n\nSo, shall we begin?\np: %d\n\n", p)))
	if err != nil {
		return
	}

	scanner := bufio.NewScanner(conn)

	_, err = conn.Write([]byte("Give me your y: "))
	if err != nil {
		return
	}
	y := new(big.Int)
	if !scanner.Scan() {
		return
	}
	_, ok := y.SetString(scanner.Text(), 10)
	if !ok {
		return
	}

	randBuffer := make([]byte, 1)
	values := make(map[string]interface{})
	C := new(big.Int)
	r := new(big.Int)
	xr := new(big.Int)
	round := 1
	for round <= totalRounds {
		_, err = conn.Write([]byte(fmt.Sprintf("Round %d/%d\n", round, totalRounds)))
		if err != nil {
			return
		}
		_, err = conn.Write([]byte("Send me value of C: "))
		if err != nil {
			return
		}

		if !scanner.Scan() {
			return
		}
		cString := scanner.Text()
		if _, exists := values[cString]; exists {
			conn.Write([]byte("Hey, no cheating!\n"))
			return
		}

		_, ok := C.SetString(cString, 10)
		if !ok {
			return
		}
		values[cString] = struct{}{}

		_, err := rand.Reader.Read(randBuffer)
		if err != nil {
			return
		}

		if randBuffer[0]&1 == 1 {
			_, err = conn.Write([]byte("Challenge A solution: "))
			if err != nil {
				return
			}

			if !scanner.Scan() {
				return
			}
			_, ok := r.SetString(scanner.Text(), 10)
			if !ok {
				return
			}

			if new(big.Int).Exp(g, r, p).Cmp(C) != 0 {
				conn.Write([]byte("Do better!\n"))
				return
			}
		} else {
			_, err = conn.Write([]byte("Challenge B solution: "))
			if err != nil {
				return
			}

			if !scanner.Scan() {
				return
			}
			_, ok := xr.SetString(scanner.Text(), 10)
			if !ok {
				return
			}

			Cy := new(big.Int).Mul(C, y)
			if Cy.Mod(Cy, p).Cmp(new(big.Int).Exp(g, xr, p)) != 0 {
				conn.Write([]byte("You lose!\n"))
				return
			}
		}

		round += 1
	}

	_, err = conn.Write([]byte(fmt.Sprintf("\n\nGood job! I can entrust you the flag: %s", flag)))
	if err != nil {
		conn.Close()
		return
	}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "1337"
	}

	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		panic(err)
	}

	p, err = rand.Prime(rand.Reader, 4096)
	if err != nil {
		panic(err)
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go session(conn)
	}
}
