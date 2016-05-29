#include <iostream>
#define MAX 100

using namespace std;

class radixsort{
    int arr[MAX],n;
    public:
    void getdata();
    void showdata();
    void sortLogic();
};

void radixsort :: getdata(){

}

void radixsort :: showdata(){

}

void radixsort(pair<int,int> *input,int N){

    int bucket[10][20][2], buck_count[10], b[10];
    int i,j,k,r,no_of_passes=0,divisor=1,largest,pass_no;

    largest = input[0].first;

    for(i=1;i<N;i++){
        if(input[i].first > largest)
            largest = input[i].first;
    }


    while(largest > 0){
        no_of_passes++;
        largest /= 10;
    }

    for(pass_no=0; pass_no < no_of_passes; pass_no++){

        for(k = 0; k < 10; k++)
            buck_count[k]=0;
            for(i = 0;i < N;i++){
                r=(input[i].first/divisor) % 10;
                bucket[r][buck_count[r]][0] = input[i].first;
                bucket[r][buck_count[r]][1] = input[i].second;
                bucket[r][buck_count[r]++][0];
        }
        i=0;
        for(k = 0; k < 10; k++){
            for(j=0; j<buck_count[k]; j++){
                input[i].first = bucket[k][j][0];
                input[i].second = bucket[k][j][1];
                i++;
            }
        }

        divisor *= 10;
    }
}

int main(){
    cout<<"\n*****Radix Sort*****\n";

    int n,a,b,i=0;

    cout<<"How many elements you require : ";
    cin>>n;
    std::pair<int,int>* arr;
    arr = new std::pair<int,int> [n];
  while(i != n){
        cin >> a >> b;
        arr[i].first = a;
        arr[i].second = b;
        i++;
    }


    radixsort(arr,n);

    cout<<"\n--Display--\n";
   for ( int i = 0; i < n; i++ )
        cout << arr[i].first << " ve " << arr[i].second<<endl;
    cout << endl;
    return 0;
}
