#!/usr/bin/env python3

print((s:=input())and min(i for i in range(14,len(s))if len({*s[i-14:i]})>13))
