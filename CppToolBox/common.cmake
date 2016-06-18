
# usage: REMOVE_ITEMS(SRC_LIST COMMON_CU_SRC)
function(REMOVE_ITEMS list1 list2)
    foreach(item in ${${list2}})
        list(REMOVE_ITEM ${list1} ${item})
    endforeach(item)
    set(${list1} ${${list1}} PARENT_SCOPE)
endfunction(REMOVE_ITEMS)
