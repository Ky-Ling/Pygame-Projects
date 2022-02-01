/*
 * @Date: 2021-10-28 09:52:02
 * @LastEditors: GC
 * @LastEditTime: 2021-10-28 10:58:48
 * @FilePath: \Pygame2-Car game\Practice.c
 */

#include <stdio.h>
#define N 5
//待排序数组
double array[N] = {2.1, 3.1, 1.5, 0.3, 7.5};
int main()
{
    //只有一个数没有间隙
    if (N < 2)
    {
        return 0;
    }
    /*对桶进行初始化*/
    //每个桶的最大值初始化了一个最小数
    //每个桶的最大值初始化了一个最小数
    //这样是为了保证至少能够被array中的最大或最小数替换掉
    //虽然定义了N个桶，但必然至少有一个桶是不会被用的
    //记录每个桶每个桶被分到的数字
    int count[N] = {0};
    //记录每个桶中最大值
    double max[N];
    //记录每个分桶中最小值
    double min[N];
    int i;
    for (i = 0; i < N; i++)
    {
        max[i] = smallest;
        min[i] = biggest;
        count[i] = 0;
    }
    /*找出梯队长度*/
    // (MAX - MIN ) / (N-1)
    double MAX = array[0], MIN = array[0];
    for (i = 1; i < N; i++)
    {
        if (array[i] > MAX)
        {
            MAX = array[i];
        }
        if (array[i] < MIN)
        {
            MIN = array[i];
        } 
    }