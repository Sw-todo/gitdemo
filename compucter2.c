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
    int Com;
    int Exp;
    struct node *link;
    }
typedef struct node ND;

void creat_poly(ND *H,int n);/*n:the polynomail items*/
void ADD(ND **H,ND **B);/*The new polynomail is storted in A*/
int main(){}/*to test the function*/
