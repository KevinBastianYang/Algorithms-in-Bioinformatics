#include<iostream>
#include<fstream>
#include<stdlib.h>
#include<cstring>
using namespace std;


class mergeSort
{
private:
	long int * array;
	long int * tmp_array;
	long int array_len;
	void sort(long int left,long int right);
public:
	mergeSort(char * file_name);//initiate array and tmp_array
	void sort();
	void merge(long int left,long int mid,long int right);
	void print();
	~mergeSort() {delete [] array;delete [] tmp_array;}
};

mergeSort::mergeSort(char * file_name)
{
	 //make sure the right parameter
	//open the file and copy it to array,array_len
	//make the same size of tmp_array
	long int n;
	long int array_pos = 0;
	char buffer[1000];
    char * tok_pos;
	fstream infile;


	infile.open(file_name,ios::in);	
    while(!infile.is_open())
    {
        cout<<"can's open "<<file_name<<"please input the file name again"<<endl;
        cin>>file_name; 
        infile.open(file_name,ios::in);	 
    }

	array = new long int[1000000];
	while(!infile.eof())
	{
		infile.getline(buffer,1000,'\n');
		tok_pos = strtok(buffer,"\t");
		while(tok_pos!=NULL)
		{
			array[array_pos++] = atoi(tok_pos);
			tok_pos = strtok(NULL,"\t");
		}
	}
	array_len = array_pos;
	tmp_array = new long int[array_len];
}



void mergeSort::sort()
{
	sort(0,array_len-1);
}

void mergeSort::sort(long int left,long int right)
{
	long int mid = (left + right) / 2;
	if(left == right) return;
	sort(left,mid);
	sort(mid+1,right);
	merge(left,mid,right);
}

void mergeSort::merge(long int left,long int mid,long int right)
{
	long int i = left, j = mid+1, k =0;
	while(i <= mid && j <= right)
	{
		if(array[i] <= array[j]) tmp_array[k++] = array[i++];
		else tmp_array[k++] = array[j++];
	}

	while(i <= mid) tmp_array[k++] = array[i++];
	while(j <= right) tmp_array[k++] = array[j++];

	for(i = 0,k=left;k<=right;) array[k++] = tmp_array[i++];
}


void mergeSort::print()
{
	for(long int i = 0;i <array_len;i++) cout<<array[i]<<' ';
	cout<<endl;
}


int main(int argc, char * argv[])
{
	char file_name[20];
	//simple check
    if(argc == 1) cout<<"Usage: ./exefile file_name"<<endl;
    else if(argc > 2) cout<<"Error: Too many parameters: Usage: ./exefile file"<<endl;
    else 
    {
    	strcpy(file_name,argv[1]);
    	mergeSort obj(file_name);
    	obj.sort();
    	obj.print();
    }
    return 0;
}
