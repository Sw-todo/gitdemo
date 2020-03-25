/*
#    COPYRIGHT SW
#    Copyright (c) 2020
#    All rights reserved
#
#    @author            :Wen
#    @name              :Wen Sun
#    @file              :/home/Sw/py_study/git/compucter2.c
#    @creation_date     :2020/03/25 09:32
#    @modification_date :2020/03/25 09:32
*/
/*solve the problem of polynomial addition*/
#include<stdio.h>
#include<stdlib.h>
#define SIZE sizeof(ND)

struct node{
    int Data;
    int Exp;
    struct node *Link;
    };
typedef struct node ND;

void create_poly(ND *H,int n);/*n:the polynomail items*/
void ADD(ND **A,ND **B);/*The new polynomail is storted in A*/
void show(ND *A);
int main(){
    int n;
    ND *A= (ND *)malloc(SIZE);;
    printf("Enter the length of the first Polynomail:\n");
    scanf("%d",&n);
    create_poly(A,n);
     ND *B= (ND *)malloc(SIZE);
    printf("Enter the length of the second Polynomail:\n");
    scanf("%d",&n);
    create_poly(B,n);
    ADD(&A,&B);
    show(A);
}/*to test the function*/
void ADD(ND **A, ND **B)/*A,B are ascending polynomails*/
{
    ND *c= (ND *)malloc(SIZE),*p,*q;
    if(*A ==0 ) {printf("A is void."); exit(0);}
    if(*B ==0 ) {printf("B is void."); exit(0);}
    if((*A)->Exp < (*B)->Exp) {c=*A;  (*A)=(*A)->Link;}
    else if((*A)->Exp > (*B)->Exp) {c=*B;  (*B)=(*B)->Link;} 
    else {c->Data=0;}
    p=c;
    while((*A)!=0 && (*B)!=0)
    {
        if(((*A)->Exp) < ((*B)->Exp))
        {  
            p->Link =(*A);
            (*A) =(*A )->Link;
            p=p->Link;
        }
         if((*A)->Exp > (*B)->Exp)
        {   
            p->Link =(*B);
            (*B) =(*B )->Link;
            p=p->Link;
        }
        if((*A)->Exp ==(*B)->Exp)
        {   
            (*A)->Data += (*B)->Data;
            ND *m;
            m=*B;
            if((*A)->Data !=0 )
            p->Link=*A;
            else{
            m=*A;
            *A=(*A)->Link;
            free(m);m=*B;}
            *B=(*B)->Link;
            free(m);
        }
    }
    while(*A){
            p->Link=(*A);
            p=p->Link;
            (*A)=(*A)->Link;
        }
    while(*B)
        {
            p->Link=(*B);
            p=p->Link;
            (*B)=(*B)->Link;
        }
    if(c->Data == 0) c=c->Link;
    (*A)=c;
}
void show(ND *A)
{
    while(A)
    {
        printf("%dx^%d+",A->Data,A->Exp);
        A=A->Link;
    }
    printf("\b \n");
}
void create_poly(ND *H,int n)
{
    ND *p=H,*q;
    int i;
    int data,exp;
    printf("Enter the value and index of the polynoamial,splited by space,in ascending order of powers:\n");
    for (i=0 ;i<n ; i++)
    {
        scanf("%d %d",&data,&exp);
        p->Data=data;
        p->Exp=exp;
        p->Link=(ND *)malloc(SIZE);
        q=p;
        p=p->Link;
    }
    q->Link=0;
    free(p);
    if (0==n) H=0;

}
