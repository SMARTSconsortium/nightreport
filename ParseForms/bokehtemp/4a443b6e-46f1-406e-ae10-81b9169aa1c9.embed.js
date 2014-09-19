console.log("embed.js");
// parseUri 1.2.2
// (c) Steven Levithan <stevenlevithan.com>
// MIT License
(function(global) {
    if(typeof(window.bokeh_embed_count) == "undefined"){
        window.bokeh_embed_count = 0;
    }
    else {
        window.bokeh_embed_count += 1;
    }
    if(window.bokeh_embed_count == 1) {
//        debugger;
    }
    var host = "";

    var staticRootUrl = "/Users/ih64/anaconda/lib/python2.7/site-packages/bokeh/server/static/";
    if (host!=""){

        staticRootUrl = "//" + host + "/bokehjs/static/";
        var bokehJSUrl = staticRootUrl + "js/bokeh.js";
    }
    else {
        bokehJSUrl = staticRootUrl +"js/bokeh.js";
    }

    var all_models = [{"attributes": {"column_names": ["x", "y"], "doc": null, "selected": [], "discrete_ranges": {}, "cont_ranges": {}, "data": {"y": [4, 9, 16, 25, 36, 49, 64, 81, 100, 121], "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}, "id": "439ded4c-3afb-450b-b057-410da3d9d96a"}, "type": "ColumnDataSource", "id": "439ded4c-3afb-450b-b057-410da3d9d96a"}, {"attributes": {"x_range": {"type": "DataRange1d", "id": "04821dd3-8876-4027-a79c-91156ae1a08f"}, "axes": [], "title": "Plot", "y_range": {"type": "DataRange1d", "id": "928dfbe2-0412-43d7-a2c9-a4e74c8d1995"}, "outer_width": 600, "renderers": [{"type": "LinearAxis", "id": "e3ee2cbe-7ced-4f6a-bf38-744442b654c8"}, {"type": "LinearAxis", "id": "8e0949b8-2f7e-4717-afa3-f1fb32ab9b4d"}, {"type": "Grid", "id": "824edabc-ee2d-429b-931a-10b277ee74aa"}, {"type": "Grid", "id": "eb7acf33-aa2a-4abd-aca8-1647b48440d4"}, {"type": "BoxSelection", "id": "817a21ae-2bce-4afb-b7d2-ff7ca6db53af"}, {"type": "BoxSelection", "id": "92f93257-6d31-486d-a990-00bb4de48617"}, {"type": "Glyph", "id": "cf13e574-2bd6-4a0a-ab2f-f51fffef8a07"}], "outer_height": 600, "doc": null, "canvas_height": 600, "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9", "tools": [{"type": "PanTool", "id": "8d7bf12e-5746-4e39-b2db-df219eb1a8b7"}, {"type": "WheelZoomTool", "id": "4b6d043c-886c-4021-94e2-40b82f8c9754"}, {"type": "BoxZoomTool", "id": "d780633f-f6d0-4e91-8f88-967cf76d6454"}, {"type": "PreviewSaveTool", "id": "1436ac2f-36ef-40b6-a40e-26d33d247dd9"}, {"type": "ResizeTool", "id": "1b8d40b4-35de-43a0-8987-b91a0b6c4425"}, {"type": "BoxSelectTool", "id": "40bb8d54-195d-4f9a-bc54-f8329087ca0c"}, {"type": "ResetTool", "id": "b888bca0-9d1c-4901-a437-f6fa573a3d8b"}], "canvas_width": 600}, "type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, {"attributes": {"data_source": {"type": "ColumnDataSource", "id": "439ded4c-3afb-450b-b057-410da3d9d96a"}, "doc": null, "id": "cf13e574-2bd6-4a0a-ab2f-f51fffef8a07", "xdata_range": null, "ydata_range": null, "glyphspec": {"line_color": {"value": "#1f77b4"}, "line_alpha": {"units": "data", "value": 1.0}, "fill_color": {"value": "#1f77b4"}, "line_width": {"units": "data", "field": "line_width"}, "fill_alpha": {"units": "data", "value": 1.0}, "text_alpha": 1.0, "text_color": "black", "y": {"units": "data", "field": "y"}, "x": {"units": "data", "field": "x"}, "type": "circle", "size": {"units": "screen", "field": null, "default": 4}}, "nonselection_glyphspec": {"line_color": {"value": "#1f77b4"}, "angle_units": "deg", "fill_color": {"value": "#1f77b4"}, "visible": null, "line_dash_offset": 0, "line_join": "miter", "size": {"units": "screen", "default": 4, "field": null}, "line_alpha": {"units": "data", "value": 0.1}, "radius_units": "screen", "end_angle_units": "deg", "valign": null, "length_units": "screen", "start_angle_units": "deg", "line_cap": "butt", "line_dash": [], "line_width": {"units": "data", "field": "line_width"}, "type": "circle", "fill_alpha": {"units": "data", "value": 0.1}, "halign": null, "y": {"units": "data", "field": "y"}, "x": {"units": "data", "field": "x"}, "margin": null}}, "type": "Glyph", "id": "cf13e574-2bd6-4a0a-ab2f-f51fffef8a07"}, {"attributes": {"sources": [{"ref": {"type": "ColumnDataSource", "id": "439ded4c-3afb-450b-b057-410da3d9d96a"}, "columns": ["y"]}], "id": "928dfbe2-0412-43d7-a2c9-a4e74c8d1995", "doc": null}, "type": "DataRange1d", "id": "928dfbe2-0412-43d7-a2c9-a4e74c8d1995"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "location": "min", "bounds": "auto", "doc": null, "id": "e3ee2cbe-7ced-4f6a-bf38-744442b654c8", "dimension": 0}, "type": "LinearAxis", "id": "e3ee2cbe-7ced-4f6a-bf38-744442b654c8"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "location": "min", "bounds": "auto", "doc": null, "id": "8e0949b8-2f7e-4717-afa3-f1fb32ab9b4d", "dimension": 1}, "type": "LinearAxis", "id": "8e0949b8-2f7e-4717-afa3-f1fb32ab9b4d"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "doc": null, "is_datetime": false, "dimension": 0, "id": "824edabc-ee2d-429b-931a-10b277ee74aa"}, "type": "Grid", "id": "824edabc-ee2d-429b-931a-10b277ee74aa"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "doc": null, "is_datetime": false, "dimension": 1, "id": "eb7acf33-aa2a-4abd-aca8-1647b48440d4"}, "type": "Grid", "id": "eb7acf33-aa2a-4abd-aca8-1647b48440d4"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "doc": null, "dimensions": ["width", "height"], "id": "8d7bf12e-5746-4e39-b2db-df219eb1a8b7"}, "type": "PanTool", "id": "8d7bf12e-5746-4e39-b2db-df219eb1a8b7"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "doc": null, "dimensions": ["width", "height"], "id": "4b6d043c-886c-4021-94e2-40b82f8c9754"}, "type": "WheelZoomTool", "id": "4b6d043c-886c-4021-94e2-40b82f8c9754"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "id": "d780633f-f6d0-4e91-8f88-967cf76d6454", "doc": null}, "type": "BoxZoomTool", "id": "d780633f-f6d0-4e91-8f88-967cf76d6454"}, {"attributes": {"sources": [{"ref": {"type": "ColumnDataSource", "id": "439ded4c-3afb-450b-b057-410da3d9d96a"}, "columns": ["x"]}], "id": "04821dd3-8876-4027-a79c-91156ae1a08f", "doc": null}, "type": "DataRange1d", "id": "04821dd3-8876-4027-a79c-91156ae1a08f"}, {"attributes": {"doc": null, "tool": {"type": "BoxZoomTool", "id": "d780633f-f6d0-4e91-8f88-967cf76d6454"}, "id": "817a21ae-2bce-4afb-b7d2-ff7ca6db53af"}, "type": "BoxSelection", "id": "817a21ae-2bce-4afb-b7d2-ff7ca6db53af"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "dataranges": [], "id": "1436ac2f-36ef-40b6-a40e-26d33d247dd9", "doc": null}, "type": "PreviewSaveTool", "id": "1436ac2f-36ef-40b6-a40e-26d33d247dd9"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "id": "1b8d40b4-35de-43a0-8987-b91a0b6c4425", "doc": null}, "type": "ResizeTool", "id": "1b8d40b4-35de-43a0-8987-b91a0b6c4425"}, {"attributes": {"doc": null, "renderers": [{"type": "Glyph", "id": "cf13e574-2bd6-4a0a-ab2f-f51fffef8a07"}], "id": "40bb8d54-195d-4f9a-bc54-f8329087ca0c"}, "type": "BoxSelectTool", "id": "40bb8d54-195d-4f9a-bc54-f8329087ca0c"}, {"attributes": {"doc": null, "tool": {"type": "BoxSelectTool", "id": "40bb8d54-195d-4f9a-bc54-f8329087ca0c"}, "id": "92f93257-6d31-486d-a990-00bb4de48617"}, "type": "BoxSelection", "id": "92f93257-6d31-486d-a990-00bb4de48617"}, {"attributes": {"plot": {"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}, "id": "b888bca0-9d1c-4901-a437-f6fa573a3d8b", "doc": null}, "type": "ResetTool", "id": "b888bca0-9d1c-4901-a437-f6fa573a3d8b"}, {"attributes": {"doc": null, "children": [{"type": "Plot", "id": "4a443b6e-46f1-406e-ae10-81b9169aa1c9"}], "id": "31db2930-a6d0-4e01-a23e-dfdc14f5b8c8"}, "type": "PlotContext", "id": "31db2930-a6d0-4e01-a23e-dfdc14f5b8c8"}];
    var modeltype = "PlotContext";
    var elementid = "3da9d45d-767c-4ece-b3e1-004eb1448018";
    var plotID = "4a443b6e-46f1-406e-ae10-81b9169aa1c9";
    var dd = {};
    dd[plotID] = all_models;
    

    var secondPlot =                 function() {
        console.log("Bokeh.js loaded callback");
        embed_core = Bokeh.embed_core;
        console.log("embed_core loaded");
        embed_core.injectCss(staticRootUrl);
        Bokeh.HasProperties.prototype.sync = Backbone.sync
        embed_core.search_and_plot(dd);
        console.log("search_and_plot called", new Date());}

    function addEvent(el, eventName, func){
        if(el.attachEvent){
            return el.attachEvent('on' + eventName, func);}
        else {
            el.addEventListener(eventName, func, false);}}
    var script_injected = !(typeof(_embed_bokeh_inject_application) == "undefined") && _embed_bokeh_inject_application;
    //var script_injected = !(typeof(_embed_bokeh_inject_application) == "undefined");
    if(typeof Bokeh == "object"){
        // application.js is already loaded
        console.log("bokeh.js is already loaded, going straight to plotting");
        setTimeout(function () {
            embed_core = Bokeh.embed_core;
            console.log("calling embed_core.search_and_plot, from already loaded bokehjs state")
            embed_core.search_and_plot(dd);}, 20);}

    else if(!script_injected){
        // bokeh.js isn't loaded and it hasn't been scheduled to be injected
        var s = document.createElement('script');
        s.async = true; s.src = bokehJSUrl; s.id="bokeh_script_tag";
        
    }
    else {
        var s = document.getElementById("bokeh_script_tag");
    }
    var local_bokeh_embed_count = window.bokeh_embed_count;
    if(typeof(s) != "undefined") {
    addEvent(
        s,'load',
        function() {
            setTimeout(secondPlot, 20 * local_bokeh_embed_count);});
    }
    if(!script_injected){
        document.body.appendChild(s);
    }

    _embed_bokeh_inject_application = true;

    window._embed_bokeh = true;}(this));