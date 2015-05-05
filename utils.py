#!/usr/bin/python
# coding: utf-8
def remove_from_list(from_list, tag_list):
    del_list = []
    for j in from_list:
        if j.text not in tag_list: 
            del_list.append(j)

    for i in del_list:
        from_list.remove(i)
