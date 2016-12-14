#! /usr/bin/env python

file = open('file.txt')
lines = file.readlines()
lines.sort()
for line in lines:
	print line ,


