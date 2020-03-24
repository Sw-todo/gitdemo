/*To  slove the first question*/
#include<stdio.h>
#include<stdlib.h>
struct node{
    int data;
    struct node *link;
    };

typedef struct node ND;

void create_list(ND **H,int n);/*creat by list n,need ND **H,who is 
                                  the first to say 1*/

void josephu(ND **H,int n,int m,int k);

int main()
{
    int n, m, k;
    ND *H=0;
    printf("Enter the value of n:\n");
    scanf("%d",&n);
    printf("Enter the value of m:\n");
    scanf("%d",&m);
    printf("Enter the value of k:\n");
    scanf("%d",&k);
    create_list(&H,n);
    josephu(&H,n,m,k);
    return 0;
}


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
void create_list(ND **H,int n)
{
    ND *p = (ND *)malloc(sizeof(ND));
    *H=p;
    int i=0;
    p->data=1;
    p->link=p;
    for (i=2;i<=n;i++)
    {
        ND *q = (ND *)malloc(sizeof(ND));
        q->data=i;
        p->link=q;
        p=p->link;
        p->link=*H;
    }

}
