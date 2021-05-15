void assert(int cond);

//gets max of array in index 0 <= i <= n
int max_array (int a[], int n){
	assert(n >= 0);
	int i, max, var1;
	max = a[0];
	for (i = 0; i < n; i++){
		assert(!((0 <= var1 && var1 < i) && !(max >= a[var1])));
		if (a[i] > max){
			max = a[i];
		}
	}
	return max;
	assert(!((0 <= var1 && var1 < n) && !(max >= a[var1])));
}

//gets max of array in index 0 <= i <= n, but with wrong invariant
int max_array_wrong (int a[], int n){
	assert(n >= 0);
	int i, max, var1;
	max = a[0];
	for (i = 0; i < n; i++){
		assert(!((0 <= var1 && var1 < n) && !(max >= a[var1])));
		if (a[i] > max){
			max = a[i];
		}
	}
	return max;
	assert(!((0 <= var1 && var1 <= n) && !(max >= a[var1])));
}

//checks if array is sorted
int is_sorted (int a[], int n){
	assert (n > 0);
	int i, var1;
	for (i = 0; i < n - 1; i++){
		assert(!((0 <= var1 && var1 < i) && !(a[var1] <= a[var1+1])));
		if (a[i] > a[i+1]){
			return 0;
			assert(a[i] == a[i+1]);
		}
	}
	return 1;
	assert(!((0 <= var1 && var1 < n - 1) && !(a[var1] <= a[var1+1])));
}

//checks if array is sorted, but implementation is wrong
int is_sorted_wrong (int a[], int n){
	assert (n > 0);
	int var1;
	if (a[i] > a[i+1]){
		return 0;
		assert(a[i] == a[i+1]);
	}
	return 1;
	assert(!((0 <= var1 && var1 < n) && !(a[var1] <= a[var1+1])));
}

//squares every entry in array and puts in array square
void square_array (int a[], int square[], int n){
	assert(n >= 0);
	int i, var1;
	for (i = 0; i < n; i++){
		assert(!((0 <= var1 && var1 < i) && !(square[var1] == a[var1]*a[var1])));
		square[i] = a[i]*a[i];
	}
	assert(!((0 <= var1 && var1 < n) && !(square[var1] == a[var1]*a[var1])));
}

//squares every entry in array and puts in array square, but with wrong invariant
void square_array_wrong (int a[], int square[], int n){
	assert(n >= 0);
	int i, var1;
	for (i = 0; i < n; i++){
		assert(square[i] == a[i]*a[i]);
		square[i] = a[i]*a[i];
	}
	assert(!((0 <= var1 && var1 < n) && !(square[var1] == a[var1]*a[var1])));
}
