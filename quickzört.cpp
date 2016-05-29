#include <iostream>
#include <vector>
using namespace std;

const int INPUT_SIZE = 4;

// A simple print function
void print(pair<int,int> *input)
{
   /*for (std::vector< pair<int,int> >::const_iterator pos = input->begin(); pos != input->end(); ++pos)
    {
        std::cout << pos->first << " " << pos->second << std::endl;
    }*/
    for ( int i = 0; i < INPUT_SIZE; i++ )
        cout <<input[i].first << " ve " << input[i].second<<endl;

}

// The partition function
int partition(pair<int,int>* input, int p, int r)
{
    int pivot = input[r].first;

    while ( p < r )
    {
        while ( input[p].first < pivot )
            p++;

        while ( input[r].first > pivot )
            r--;

        if ( input[p].first == input[r].first )
            p++;
        else if ( p < r )
        {
            pair<int,int> tmp;
            tmp.first = input[p].first;
            tmp.second = input[p].second;
            input[p].first = input[r].first;
            input[p].second = input[r].second;
            input[r].first = tmp.first;
            input[r].second = tmp.second;
        }
    }

    return r;
}

// The quicksort recursive function
void quicksort(pair<int,int> *input, int p, int r)
{
    if ( p < r )
    {
        int j = partition(input, p, r);
        quicksort(input, p, j-1);
        quicksort(input, j+1, r);
    }

}

int main()
{
    std::pair<int,int>* input;
    input = new std::pair<int,int> [INPUT_SIZE];
    std::pair<int,int>* LastStandings;
    LastStandings = new std::pair<int,int> [INPUT_SIZE];
    vector< pair<int,int> > Points;
    int i = 0;
    int a,b;
    while(i != INPUT_SIZE){
        cin >> a >> b;
        input[i].first = a;
        input[i].second = b;
        i++;
    }
    cout << "Input: ";
    //print(input);
    quicksort(input, 0, 3);
    int i2 = INPUT_SIZE;
    int i1 = 0;

    while(i1 != INPUT_SIZE){
    if(input[i1].first != input[i1+1].first){
        Points.push_back(std::make_pair(i2,input[i1].second));
        i1++;
        i2--;
    }
    else{
        Points.push_back(std::make_pair(i2,input[i1].second));
        i1++;
    }
}

    std::vector< pair<int,int> >::iterator k;
    std::vector< pair<int,int> >::iterator l;
    int k1;
    for (k = Points.begin(),l = Points.begin(),k1 = 0 ;k1 != INPUT_SIZE; k++,k1++)
    {
        LastStandings[k1].second = k->second;
        LastStandings[k1].first = 0;
        l = k;
        while(l != Points.end()){

            if(k->second == l->second){
                LastStandings[k1].first += (l->first);
                l++;
            }
            else
                l++;
        }
    }



    cout << "Output: ";
    print(LastStandings);
    return 0;
}
