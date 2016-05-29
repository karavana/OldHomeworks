#include <iostream>
using namespace std;

void shellsort(pair<int,int> *array,int N){
    int increment,j;
    pair<int,int> temp;
        for(increment = N/2;increment > 0; increment /= 2)
        {
                for(int i = increment; i<N; i++)
                {
                        temp.first = array[i].first;
                        temp.second = array[i].second;

                        for(j = i; j >= increment ;j-=increment)
                        {
                                if(temp.first < array[j-increment].first)
                                {
                                        array[j].first = array[j-increment].first;
                                        array[j].second = array[j-increment].second;
                                }
                                else
                                {
                                        break;
                                }
                        }
                        array[j].first = temp.first;
                        array[j].second = temp.second;
                }
        }
}

int main(void)
{
    int N = 4;
    int i = 0;
    int a,b,i1=0;
    std::pair<int,int>* array;
    array = new std::pair<int,int> [N];
    while(i != N){
        cin >> a >> b;
        array[i].first = a;
        array[i].second = b;
        i++;
    }
    shellsort(array,N);
    cout<<"After Sorting:";
    for(i1=0;i1<4;i1++){
        cout<<array[i1].first <<" ve "<< array[i1].second <<endl;
    }

}
