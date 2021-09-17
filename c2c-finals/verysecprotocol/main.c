#include <stdio.h>

int main() {
	long p = 2272978429;
	long target_b = 1042188408;

	for (long b_test = 1; b_test < p; b_test++) {
		if ((1 << b_test) % p == target_b) {
			printf("FOUND b: %d\n", b_test);
		}
	}
}
