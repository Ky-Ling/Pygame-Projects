/*
 * @Date: 2021-10-28 09:52:02
 * @LastEditors: GC
 * @LastEditTime: 2021-10-28 10:58:48
 * @FilePath: \Pygame2-Car game\Practice.c
 */

#include <stdio.h>
#define N 5
//����������
double array[N] = {2.1, 3.1, 1.5, 0.3, 7.5};
int main()
{
    //ֻ��һ����û�м�϶
    if (N < 2)
    {
        return 0;
    }
    /*��Ͱ���г�ʼ��*/
    //ÿ��Ͱ�����ֵ��ʼ����һ����С��
    //ÿ��Ͱ�����ֵ��ʼ����һ����С��
    //������Ϊ�˱�֤�����ܹ���array�е�������С���滻��
    //��Ȼ������N��Ͱ������Ȼ������һ��Ͱ�ǲ��ᱻ�õ�
    //��¼ÿ��Ͱÿ��Ͱ���ֵ�������
    int count[N] = {0};
    //��¼ÿ��Ͱ�����ֵ
    double max[N];
    //��¼ÿ����Ͱ����Сֵ
    double min[N];
    int i;
    for (i = 0; i < N; i++)
    {
        max[i] = smallest;
        min[i] = biggest;
        count[i] = 0;
    }
    /*�ҳ��ݶӳ���*/
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