#include<iostream>
#include<fstream>
#include<stdlib.h>
#include<cstring>
using namespace std;


class insertionSort
{
private:
	long int * array;
	long int array_len;
public:
	insertionSort(char *file_name);
	void sort();
	void print();
	~insertionSort() {delete [] array;}
};

insertionSort::insertionSort(char * file_name)
{
	 //read file and get array
	long int n;
	long int array_pos = 0;
	int str_pos = 0;
	char temp;
	char str_tmp[20];
    long int counter = 0;
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
}


void insertionSort::sort()
{
	long int i,j,tmp;
	for(i = 1;i < array_len;i++)
	{
		tmp = array[i];
		for(j = i - 1; j >= 0 && array[j] > tmp;j--) array[j+1] = array[j];
		array[j+1] = tmp;
	}
}

void insertionSort::print()
{
	int i;
	for(i =0;i< array_len;i++) cout<<array[i]<<' ';
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
    	insertionSort obj(file_name);
    	obj.sort();
    	obj.print();
    }
    return 0;
}
