void assert(int cond);
#define SWAP(X,Y) { tmp = (X); (X) = (Y); (Y) = tmp; }

//gets max of array in index 0 <= i <= n
int max_array (int a[], int n){
	assert(n >= 0);
	int i, max, var1, var2;
	max = a[0];
	for (i = 0; i < n; i++){
		assert(!(0 <= var1 <= i && !(max >= a[var1])));
		if (a[i] > max){
			max = a[i];
		}
	}
	return max;
	assert(!(0 <= var2 <= n && !(max >= a[var2])));
}

//sorts array in range 0 <= i < n
int bubble_sort (int a[], int n){
	assert(n >= 0);
	int i, j, tmp, var1, var2, var3, var4, var5, var6;
	for (i = 0; i < n-1; i++){
		assert (!(n-i <= var1 < n && !(!(0 <= var2 < n-i && !(a[var1] >= a[var2])))) &&
				!((n-i <= var3 < n && n-i <= var4 < n && var3 <= var4) && !(a[var3] <= a[var4])));
		for (j = 0; j < n-i-1; j++){
			assert (!(0 <= var3 < j && !(a[j] >= a[var3])));
			if (a[j] > a[j+1]) SWAP (a[j], a[j+1])
		}
	}
	assert (!(((0 <= var5 < n) && (0 <= var6 < n) && (var5 <= var6)) && !(a[var5] <= a[var6])));
}

//sorts array in range 0 <= i < n, but with an intentionally wrong loop invariant
int bubble_sort_wrong (int a[], int n){
	assert(n >= 0);
	int i, j, tmp, var1, var2, var3, var4, var5, var6;
	for (i = 0; i < n-1; i++){
		assert (!(n-i <= var1 < n && !(!(0 <= var2 < n-i && !(a[var1] >= a[var2])))) &&
				!((n-i <= var3 < n && n-i <= var4 < n && var3 <= var4) && !(a[var3] <= a[var4])));
		for (j = 0; j < n-i-1; j++){
			assert (!(0 <= var3 < i && !(a[j] >= a[var3])));
			if (a[j] > a[j+1]) SWAP (a[j], a[j+1])
		}
	}
	assert (!(((0 <= var5 < n) && (0 <= var6 < n) && (var5 <= var6)) && !(a[var5] <= a[var6])));
}

//takes a sorted array and finds i so that a[i] == x. If no such i exists, returns -1
int binary_search (int a[], int n, int x){
	assert (!(n >= 0 && (((0 <= var1 < n) && (0 <= var2 < n) && (var1 <= var2)) && !(a[var1] <= a[var2]))));
	int start, end, mid, var1, var2, var3;
	start = 0;
	end = n - 1;
	mid = (start+end)/2;
	while (start <= end){
		assert (!(a[mid] == x && !(start <= mid <= end)));
		if (a[mid] == x){
			return mid;
			assert (a[mid] == x);
		}
		else {
			if (a[mid] < x){
				start = mid+1;
			}
			else { //a[mid] > x
				end = mid-1;
			}
		}
		mid = (start+end)/2;
	}
	return -1;
	assert (!(0 <= var3 < n && !(a[var3] != x)));
}
