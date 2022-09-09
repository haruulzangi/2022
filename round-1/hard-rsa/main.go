package main

import (
	"crypto/rand"
	"crypto/sha256"
	"fmt"
	"hash"
	"io"
	"math/big"
)

const (
	flag = "HZ{RS@_1s_cl@SSIc_GGh9sJlMGryCfpY}"
)

// incCounter increments a four byte, big-endian counter.
func incCounter(c *[4]byte) {
	if c[3]++; c[3] != 0 {
		return
	}
	if c[2]++; c[2] != 0 {
		return
	}
	if c[1]++; c[1] != 0 {
		return
	}
	c[0]++
}

// mgf1XOR XORs the bytes in out with a mask generated using the MGF1 function
// specified in PKCS #1 v2.1.
func mgf1XOR(out []byte, hash hash.Hash, seed []byte) {
	var counter [4]byte
	var digest []byte

	done := 0
	for done < len(out) {
		hash.Write(seed)
		hash.Write(counter[0:4])
		digest = hash.Sum(digest[:0])
		hash.Reset()

		for i := 0; i < len(digest) && done < len(out); i++ {
			out[done] ^= digest[i]
			done++
		}
		incCounter(&counter)
	}
}

func pubKeySize(N *big.Int) int {
	return (N.BitLen() + 7) / 8
}

func computeOAEP(k int, msg []byte, label []byte) []byte {
	hash := sha256.New()

	if len(msg) > k-2*hash.Size()-2 {
		panic("computeOAEP: message is too long")
	}

	hash.Write(label)
	lHash := hash.Sum(nil)
	hash.Reset()

	em := make([]byte, k)
	seed := em[1 : 1+hash.Size()]
	db := em[1+hash.Size():]

	copy(db[0:hash.Size()], lHash)
	db[len(db)-len(msg)-1] = 1
	copy(db[len(db)-len(msg):], msg)

	_, err := io.ReadFull(rand.Reader, seed)
	if err != nil {
		panic(err)
	}

	mgf1XOR(db, hash, seed)
	mgf1XOR(seed, hash, db)

	return em
}

func main() {
	p, err := rand.Prime(rand.Reader, 2048)
	if err != nil {
		panic(err)
	}
	q, err := rand.Prime(rand.Reader, 2048)
	if err != nil {
		panic(err)
	}

	n := new(big.Int).Mul(p, q)
	fmt.Println("n:", n)
	e1 := big.NewInt(3)
	fmt.Println("e1:", e1)
	e2 := big.NewInt(0x10001)
	fmt.Println("e2:", e2)

	plaintext := computeOAEP(pubKeySize(n), []byte(flag), nil)
	m := new(big.Int).SetBytes(plaintext)
	c1 := new(big.Int).Exp(m, e1, n)
	c2 := new(big.Int).Exp(m, e2, n)

	fmt.Println("c1:", c1)
	fmt.Println("c2:", c2)
}
