(function(root) {
    var Map = {},
        layers;

    Map = function(el, l, callback) {
        MM_map = mapbox.map(el);
        MM_map.addLayer(mapbox.layer().id(l.api));

        for (var i = 0; i < l.features.length; i++) {
            switch(l.features[i]) {
                case 'zoomer':
                    MM_map.ui.zoomer.add();
                    break;
                case 'zoombox':
                    MM_map.ui.zoombox.add();
                    break;
                case 'legend':
                    MM_map.legend = MM_map.ui.legend.add();
                    break;
                case 'attribution':
                    MM_map.ui.attribution.add();
                    break;
                case 'interaction':
                    MM_map.interaction.auto();
                    break;
                case 'pointselector':
                    MM_map.ui.pointselector.add();
                    break;
                case 'hash':
                    MM_map.ui.hash.add();
                    break;
                case 'fulllscreen':
                    MM_map.ui.fullscreen.add();
                    break;
            }
        }
        MM_map.refresh()
        MM_map.setZoomRange(l.zoomRange[0],l.zoomRange[1])
        MM_map.centerzoom(l.center, l.center.zoom);
        default_center = l.center;
        default_zoom = l.center.zoom

        return Map;
    }

    Map.layers = function(x) {
    }

    Map.markers = function () {
        $.getJSON('features/obras/', function(data) {
            var markerLayer = mapbox.markers.layer().features(data.features).factory(function(f){
                var d = document.createElement('div');
                d.className = 'mmg mmg-' + (ICONS[f.properties.producto] ? ICONS[f.properties.producto] : 'default');
                // Add function that centers marker on click
                MM.addEvent(d, 'click', function(e) {
                    MM_map.ease.location({
                        lat: f.geometry.coordinates[1],
                        lon: f.geometry.coordinates[0]
                    }).zoom(15).optimal();
                });
                return d;
            });
            var interaction = mapbox.markers.interaction(markerLayer);
            MM_map.addLayer(markerLayer)

            interaction.formatter(function(feature) {
                var o =  GRUPO[feature.properties.grupo][0] + '<br/>';
                $.each(feature.properties, function(key, val) {
                    if (key != 'grupo')
                        o += '<b>' + key.toUpperCase() + ':</b> ' + val + '<br/>';
                    else {
                        o += '<b>PROYECTO:</b> ' + GRUPO[val][1] + '<br/>';
                    }
                });

                return o;
            });
            $.gritter.add({title:'Obras',text: (data.features.length) + ' Obras desplegadas'})
        })
    }

    Map.filters = function() {
        var pobj = this;
        $("[name='prod_check']").click(function(ev) {
            if (ev.target.value == "Todos") {
                $("[name='prod_check']").each(function(o,i){i.checked = ev.target.checked});
            }
            else {
                $("#chkTodos").checked = false;
            }
            setTimeout(function() {
                MM_map.getLayer("markers").filter(pobj.doFilter);
            },10)
        });
        $("[name='proj_check']").click(function(ev) {
            if (ev.target.value == "Todos") {
                $("[name='proj_check']").each(function(o,i){i.checked = ev.target.checked});
            }
            else {
                $("#chkTodosP").checked = false;
            }
            setTimeout(function() {
                MM_map.getLayer("markers").filter(pobj.doFilter);
            },10)
        });
    }

    Map.doFilter = function(f) {
        vals = $("[name='prod_check']").map(function(o,i){if (i.value != "Todos" && i.checked) return i.value}).toArray();
        val1 = vals.length > 0 && vals.indexOf(f.properties['producto']) != -1
        vals = $("[name='proj_check']").map(function(o,i){if (i.value != "Todos" && i.checked) return i.value}).toArray();
        val2 = vals.length > 0 && vals.indexOf(GRUPO[f.properties['grupo']][1]) != -1
        return val1 && val2
    }

    Map.selects = function() {
        $("[name='departamento']").change(function (ev) {
            if (ev.target.value != "Ninguno") {
                vals = ev.target.value.split(",");
                MM_map.setExtent([{lat:Number(vals[1]) , lon: Number(vals[0])},
                    {lat: Number(vals[3]), lon:Number(vals[2])}]);
                var sel = ev.target.selectedIndex
                $.gritter.add({title:'Departamento',text: ev.target.options[sel].text + ' escogido'});
            }
            else
                MM_map.centerzoom(default_center, default_zoom);
        });
    }
    root.Map = Map;
})(this);
/* GRITTER */
(function(b){b.gritter={};b.gritter.options={position:"",class_name:"",fade_in_speed:"medium",fade_out_speed:1000,time:6000};b.gritter.add=function(f){try{return a.add(f||{})}catch(d){var c="Gritter Error: "+d;(typeof(console)!="undefined"&&console.error)?console.error(c,f):alert(c)}};b.gritter.remove=function(d,c){a.removeSpecific(d,c||{})};b.gritter.removeAll=function(c){a.stop(c||{})};var a={position:"",fade_in_speed:"",fade_out_speed:"",time:"",_custom_timer:0,_item_count:0,_is_setup:0,_tpl_close:'<div class="gritter-close"></div>',_tpl_title:'<span class="gritter-title">[[title]]</span>',_tpl_item:'<div id="gritter-item-[[number]]" class="gritter-item-wrapper [[item_class]]" style="display:none"><div class="gritter-top"></div><div class="gritter-item">[[close]][[image]]<div class="[[class_name]]">[[title]]<p>[[text]]</p></div><div style="clear:both"></div></div><div class="gritter-bottom"></div></div>',_tpl_wrap:'<div id="gritter-notice-wrapper"></div>',add:function(g){if(typeof(g)=="string"){g={text:g}}if(!g.text){throw'You must supply "text" parameter.'}if(!this._is_setup){this._runSetup()}var k=g.title,n=g.text,e=g.image||"",l=g.sticky||false,m=g.class_name||b.gritter.options.class_name,j=b.gritter.options.position,d=g.time||"";this._verifyWrapper();this._item_count++;var f=this._item_count,i=this._tpl_item;b(["before_open","after_open","before_close","after_close"]).each(function(p,q){a["_"+q+"_"+f]=(b.isFunction(g[q]))?g[q]:function(){}});this._custom_timer=0;if(d){this._custom_timer=d}var c=(e!="")?'<img src="'+e+'" class="gritter-image" />':"",h=(e!="")?"gritter-with-image":"gritter-without-image";if(k){k=this._str_replace("[[title]]",k,this._tpl_title)}else{k=""}i=this._str_replace(["[[title]]","[[text]]","[[close]]","[[image]]","[[number]]","[[class_name]]","[[item_class]]"],[k,n,this._tpl_close,c,this._item_count,h,m],i);if(this["_before_open_"+f]()===false){return false}b("#gritter-notice-wrapper").addClass(j).append(i);var o=b("#gritter-item-"+this._item_count);o.fadeIn(this.fade_in_speed,function(){a["_after_open_"+f](b(this))});if(!l){this._setFadeTimer(o,f)}b(o).bind("mouseenter mouseleave",function(p){if(p.type=="mouseenter"){if(!l){a._restoreItemIfFading(b(this),f)}}else{if(!l){a._setFadeTimer(b(this),f)}}a._hoverState(b(this),p.type)});b(o).find(".gritter-close").click(function(){a.removeSpecific(f,{},null,true)});return f},_countRemoveWrapper:function(c,d,f){d.remove();this["_after_close_"+c](d,f);if(b(".gritter-item-wrapper").length==0){b("#gritter-notice-wrapper").remove()}},_fade:function(g,d,j,f){var j=j||{},i=(typeof(j.fade)!="undefined")?j.fade:true,c=j.speed||this.fade_out_speed,h=f;this["_before_close_"+d](g,h);if(f){g.unbind("mouseenter mouseleave")}if(i){g.animate({opacity:0},c,function(){g.animate({height:0},300,function(){a._countRemoveWrapper(d,g,h)})})}else{this._countRemoveWrapper(d,g)}},_hoverState:function(d,c){if(c=="mouseenter"){d.addClass("hover");d.find(".gritter-close").show()}else{d.removeClass("hover");d.find(".gritter-close").hide()}},removeSpecific:function(c,g,f,d){if(!f){var f=b("#gritter-item-"+c)}this._fade(f,c,g||{},d)},_restoreItemIfFading:function(d,c){clearTimeout(this["_int_id_"+c]);d.stop().css({opacity:"",height:""})},_runSetup:function(){for(opt in b.gritter.options){this[opt]=b.gritter.options[opt]}this._is_setup=1},_setFadeTimer:function(f,d){var c=(this._custom_timer)?this._custom_timer:this.time;this["_int_id_"+d]=setTimeout(function(){a._fade(f,d)},c)},stop:function(e){var c=(b.isFunction(e.before_close))?e.before_close:function(){};var f=(b.isFunction(e.after_close))?e.after_close:function(){};var d=b("#gritter-notice-wrapper");c(d);d.fadeOut(function(){b(this).remove();f()})},_str_replace:function(v,e,o,n){var k=0,h=0,t="",m="",g=0,q=0,l=[].concat(v),c=[].concat(e),u=o,d=c instanceof Array,p=u instanceof Array;u=[].concat(u);if(n){this.window[n]=0}for(k=0,g=u.length;k<g;k++){if(u[k]===""){continue}for(h=0,q=l.length;h<q;h++){t=u[k]+"";m=d?(c[h]!==undefined?c[h]:""):c[0];u[k]=(t).split(l[h]).join(m);if(n&&u[k]!==t){this.window[n]+=(t.length-u[k].length)/l[h].length}}}return p?u:u[0]},_verifyWrapper:function(){if(b("#gritter-notice-wrapper").length==0){b("body").append(this._tpl_wrap)}}}})(jQuery);