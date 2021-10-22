void assert(int cond);
void assume(int cond);



//example from lecture
void example (int x, int y){
	assume (y > 0);
	int z = x;
	int i = 0;
	while (i < y){
		z = z + 1;
		i = i + 1;
	}
	assert (z == x + y);
}

//example from lecture with invariant prewritten
void example_with_invariant (int x, int y){
	assume (y > 0);
	int z = x;
	int i = 0;
	while (i < y){
		assume (z == x+i && z <= x+y);
		z = z + 1;
		i = i + 1;
	}
	assert (z == x + y);
}

//add x to y using two loops
void addition_with_two_loops (int x, int y){
	assume (x > 0 && y > 0);
	int z = 0;
	int i, j;
	for (i = 0; i < x; i++){
		z++;
	}
	for (j = 0; j < y; j++){
		z++;
	}
	assert (z == x + y);
}

//find max in array
int max_array (int a[], int n){
	assume(n >= 0);
	int i, max, ghost;
	max = a[0];
	for (i = 0; i < n; i++){
		if (a[i] > max){
			max = a[i];
		}
	}
	return max;
	assert(!((0 <= ghost && ghost < n) && !(max >= a[ghost])));
}

//squares every entry in array a and puts in array square
void square_array (int a[], int square[], int n){
	assume(n >= 0);
	int i, ghost;
	for (i = 0; i < n; i++){
		square[i] = a[i]*a[i];
	}
	assert(!((0 <= ghost && ghost < n) && !(square[ghost] == a[ghost]*a[ghost])));
}

//checks if array is sorted
int is_sorted (int a[], int n){
	assume (n > 0);
	int i, ghost;
	for (i = 0; i < n - 1; i++){
		if (a[i] > a[i+1]){
			return 0;
			assert(a[i] > a[i+1]);
		}
	}
	return 1;
	assert(!((0 <= ghost && ghost < n - 1) && !(a[ghost] <= a[ghost+1])));
}

//multiply x by y
void multiplication_with_nested_loops (int x, int y) {
	assume (x > 0 && y > 0);
	int z = 0;
	int i, j;
	for (i = 0; i < x; i++){
		for (j = 0; j < y; j++){
			z++;
		}
	}
	assert (z == x * y);
}


//multiply x by y
void multiplication_with_nested_loops_and_invariant (int x, int y) {
	assume (x > 0 && y > 0);
	int z = 0;
	int i, j;
	for (i = 0; i < x; i++){
		assume(z == y*i && z <= x*y);
		for (j = 0; j < y; j++){
			z++;
		}
	}
	assert (z == x * y);
}

//checks if array has duplicates
int contains_duplicates(int a[], int n){
	assume (n > 0);
	int i, j, ghost1, ghost2;
	for (i = 0; i < n; i++){
		for (j = 0; j < n; j++){
			if (!(i == j) && a[i] == a[j]){
				return 0;
				assert(!(i == j) && a[i] == a[j]);
			}
		}
	}
	return 1;
	assert(!((0 <= ghost1 && ghost1 < n - 1) && (0 <= ghost2 && ghost2 < n - 1) && !(ghost1 == ghost2) && (a[ghost1] == a[ghost2])));
}

//multiply x by y
void multiplication (int x, int y) {
	assume (x > 0 && y > 0);
	int z = 0;
	int i;
	for (i = 0; i < x; i++){
		z = z + y;
	}
	assert (z == x * y);
}

//multiply x by y with invariant
void multiplication_with_invariant (int x, int y) {
	assume (x > 0 && y > 0);
	int z = 0;
	int i;
	for (i = 0; i < x; i++){
		assume (z == y*i && z <= x*y);
		z = z + y;
	}
	assert (z == x * y);
}

//bubble sort
void bubble_sort (int a[], int n){
	assume (n > 0);
	int ghost;
	int tmp;
	int i, j;
	for (i = 0; i < n-1; i++){
		for (j = 0; j < n-i-1; j++){
			if (a[j] > a[j+1]) {
				tmp = a[j];
				a[j] = a[j+1];
				a[j+1] = tmp;
			}
		}
	}
	assert(!((0 <= ghost && ghost < n-1) && !(a[ghost]<=a[ghost+1])));
}

//bubble sort with invariants
void bubble_sort_with_invariant (int a[], int n){
	assume (n > 0);
	int ghost;
	int tmp;
	int i, j;
	for (i = 0; i < n-1; i++){
		assume(!(n-i-1 <= ghost && ghost < n-1) || a[ghost]<=a[ghost+1]);
		for (j = 0; j < n-i-1; j++){
			assume(!(0 <= ghost && ghost < j) || a[ghost]<=a[j]);
			if (a[j] > a[j+1]) {
				tmp = a[j];
				a[j] = a[j+1];
				a[j+1] = tmp;
			}
		}
	}
	assert(!((0 <= ghost && ghost < n-1) && !(a[ghost]<=a[ghost+1])));
}
