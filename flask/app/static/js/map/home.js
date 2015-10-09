function get_cookie(name){
  var r = document.cookie.match("\\b"+name+"=([^;]*)\\b");
    //alert('r:'+r)
  return r?r[1]:undefined;
}

function add_markers(map, lng, lat){
  var posting = $.post("/addmarkers", 
                       {"lng":lng, "lat":lat, "_xsrf":get_cookie("_xsrf")});
  posting.done(function(data){
    alert("add markers sucess!");
    get_markers(map);
  });

  posting.fail(function(){
    alert("Error: can not add markers.");
  });
}


function get_markers(map,lon,lat){
  //删除所有overlays
  map.clearOverlays();
  //从后端获取数据，重新生成marker
  if(lon)
    {var posting = $.post("/getmarkers1", {"points":lon.toString()+','+lat.toString()});}
  else
    {var posting = $.post("/getmarkers");}
  //alert(data);
  posting.done(function(data){
    var dataObj = eval("("+data+")");
      //alert(dataObj);
    //生成marker
    for(var x in dataObj){
      lng = parseFloat(dataObj[x]["lon"]);
      //alert(lng);
      lat = parseFloat(dataObj[x]["lat"]);
      value = parseFloat(dataObj[x]["RSRP"]);
        //alert('##########'+value.toString());
      var p = new BMap.Point(lng, lat);
      if (value<-100)
      {
          //alert('SU');
          var myIcon = new BMap.Icon("/static/images/red.png", new BMap.Size(28, 28));
      }
      else{
          //alert('FA');
          var myIcon = new BMap.Icon("/static/images/green.png", new BMap.Size(28, 28));
      }

      overlay = new BMap.Marker(p, {icon:myIcon});
      //在overlay配置marker信息。
      overlay.mp_info = 
        {uid:dataObj[x]["RSRP"],
         lng:dataObj[x]["lon"],
         lat:dataObj[x]["lat"],
        };

      //鼠标悬停效果
      overlay.addEventListener("mouseover", 
                               function(){
                                 var opts = {width : 200, height: 60, enableMessage:false, 
                                             enableAutoPan:false}
                                 var infostr = this.mp_info["uid"];
                                 var infoWindow = new BMap.InfoWindow(infostr, opts);
                                 this.openInfoWindow(infoWindow);
                               }
                              );
      overlay.addEventListener("mouseout", 
                                function(){this.closeInfoWindow();}
                              );

      //把marker加到map上
      map.addOverlay(overlay);
    }
    //从图上重新读取markers，更新右侧的content。
    var overlays = map.getOverlays();
    var markers = [];
    for(var x in overlays){
      if(overlays[x] instanceof BMap.Marker){
        markers.push(overlays[x]);
      }
    }
  });

  posting.fail(function(){
    alert("Error: can not update markers.");
  });
}


