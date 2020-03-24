/*To  slove the first question*/
#include<stdio.h>
#include<stdlib.h>
struct node{
    int data;
    struct node *link;
    };

typedef struct node ND;

void creat_list(ND **H,int n[]);/*creat by list n,need ND **H,who is 
                                  the first to say 1*/

void josephu(ND **H,int n,int m,int k);

void josephu(ND **H,int n,int m,int k)/*total = n,start at k*/
{
    ND *p=*H,*q;
    int i=0;
    printf("Pop these people by order:\n");
    for (i=1;i<n+k-1;i++) p=p->link;/*to find the one before who say 1 when game begin*/
    while ((*H)->link != *H )
    {
        for(i=1; i<m;i++) p=p->link;/*find the one who is going to be popped*/
        q=p; p=p->link; q->link = p->link; 
        printf("pop:%5d\n",p->data); free(p);
        p=q; *H=q;
    }
    printf("The last one:%5d",(*H)->data);
    free(*H);

}
