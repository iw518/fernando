/**
 * Created by Administrator on 2017/3/3 0003.
 */
function expand_section_info(section) {
    var items = section.items;
    var section_info_list = [];
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        section_info_list.push(expand_hole_info(item));
    }
    return section_info_list;
}

function expand_hole_info(item) {
    var hole = item.hole;
    var distance = item.distance;
    var info_list = [];
    info_list.push(hole.holeName, distance.toFixed(2), hole._Hole__Dep.toFixed(2), hole.elevation.toFixed(2));
    if (hole.waterLevel > 0) {
        info_list.push(hole.waterLevel.toFixed(2));

    }
    else {
        info_list.push('');
    }
    for (var i = 0; i < hole.layers.length; i++) {
        var layer = hole.layers[i];
        if (layer.thickness > 0) {
            info_list.push(layer.endDep.toFixed(2));
        }
        else {
            info_list.push(0.00);
        }
    }
    return info_list;
}
