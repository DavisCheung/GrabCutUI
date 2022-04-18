// Taken from script-tutorials.com. Adjusted for GrabCutWeb.
//  Added a function to return selection values by jQuery
//  Made entire file scale with large images (fixes width to 600px max)
//
// Whoever wrote this originally did not make it very friendly to edit
//
// variables
var canvas, ctx;
var image;
var iMouseX, iMouseY = 1;
var theSelection;
var scale = 1; // Scaling factor for images that are too large
// define Selection constructor
function Selection(x, y, w, h){
    this.x = x; // initial positions
    this.y = y;
    this.w = w; // and size
    this.h = h;
    this.px = x; // extra variables to dragging calculations
    this.py = y;
    this.csize = 6; // resize cubes size
    this.csizeh = 10; // resize cubes size (on hover)
    this.bHow = [false, false, false, false]; // hover statuses
    this.iCSize = [this.csize, this.csize, this.csize, this.csize]; // resize cubes sizes
    this.bDrag = [false, false, false, false]; // drag statuses
    this.bDragAll = false; // drag whole selection
}
// define Selection draw method
Selection.prototype.draw = function(){
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    xPos = this.x;
    yPos = this.y;
    wPos = this.w;
    hPos = this.h;
    /*
    if(this.w > 600){
        wPos = 600;
        hPos = this.h / (this.w/wPos);
        xPos = this.x / (this.w/wPos);
        yPos = this.y / (this.w/wPos);
    }*/
    ctx.strokeRect(xPos, yPos, wPos, hPos);
    // draw part of original image
    if (this.w > 0 && this.h > 0) {
        ctx.drawImage(image, xPos*scale, yPos*scale, wPos*scale, hPos*scale, xPos, yPos, wPos, hPos);
    }
    // draw resize cubes
    ctx.fillStyle = '#fff';
    ctx.fillRect(xPos - this.iCSize[0], yPos - this.iCSize[0], this.iCSize[0] * 2, this.iCSize[0] * 2);
    ctx.fillRect(xPos + wPos - this.iCSize[1], yPos - this.iCSize[1], this.iCSize[1] * 2, this.iCSize[1] * 2);
    ctx.fillRect(xPos + wPos - this.iCSize[2], yPos + hPos - this.iCSize[2], this.iCSize[2] * 2, this.iCSize[2] * 2);
    ctx.fillRect(xPos - this.iCSize[3], yPos + hPos - this.iCSize[3], this.iCSize[3] * 2, this.iCSize[3] * 2);
}
function drawScene() { // Input preview
    var ctxWidth = ctx.canvas.width;
    var ctxHeight = ctx.canvas.height;
    ctx.clearRect(0, 0, ctxWidth, ctxHeight); // clear canvas
    // draw source image
    ctx.drawImage(image, 0, 0, ctxWidth, ctxHeight);
    // and make it darker
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, ctxWidth, ctxHeight);
    // draw selection
    theSelection.draw();
}
$(function(){
    // loading source image
    image = new Image();
    image.onload = function () {
    }
    image.id = "inImg";
    image.src = document.getElementById('selection').className; // An abosolutely disgustingly hacky way to pass a Jinja variable.
                                                                // If you are a prospective employer reading this, I promise I won't
                                                                //   write such code in the future
    image.style = "max-width: 600px";
    defSelW = document.getElementById('selection').width;
    defSelh = document.getElementById('selection').height;
    canvas = document.getElementById('selection');
    if (defSelW > 600) {  // Image larger than 600px
        scale = defSelW / 600;
        canvas.width = 600;
        canvas.height = canvas.height/scale;
    }
    ctx = canvas.getContext('2d');
    // create initial selection
    theSelection = new Selection(50, 50, 50, 50);
    //theSelection = new Selection(defSelW/50, defSelW/50, defSelW/4, defSelh/4);
    theSelection.csize = document.getElementById('selection').width / 80;
    theSelection.csizeh = document.getElementById('selection').width / 70;
    $('#selection').mousemove(function(e) { // binding mouse move event
        var canvasOffset = $(canvas).offset();
        iMouseX = Math.floor(e.pageX - canvasOffset.left);
        iMouseY = Math.floor(e.pageY - canvasOffset.top);
        // in case of drag of whole selector
        if (theSelection.bDragAll) {
            theSelection.x = iMouseX - theSelection.px;
            theSelection.y = iMouseY - theSelection.py;
        }
        for (i = 0; i < 4; i++) {
            theSelection.bHow[i] = false;
            theSelection.iCSize[i] = theSelection.csize;
        }
        // hovering over resize cubes
        if (iMouseX > theSelection.x - theSelection.csizeh && iMouseX < theSelection.x + theSelection.csizeh &&
            iMouseY > theSelection.y - theSelection.csizeh && iMouseY < theSelection.y + theSelection.csizeh) {
            theSelection.bHow[0] = true;
            theSelection.iCSize[0] = theSelection.csizeh;
        }
        if (iMouseX > theSelection.x + theSelection.w-theSelection.csizeh && iMouseX < theSelection.x + theSelection.w + theSelection.csizeh &&
            iMouseY > theSelection.y - theSelection.csizeh && iMouseY < theSelection.y + theSelection.csizeh) {
            theSelection.bHow[1] = true;
            theSelection.iCSize[1] = theSelection.csizeh;
        }
        if (iMouseX > theSelection.x + theSelection.w-theSelection.csizeh && iMouseX < theSelection.x + theSelection.w + theSelection.csizeh &&
            iMouseY > theSelection.y + theSelection.h-theSelection.csizeh && iMouseY < theSelection.y + theSelection.h + theSelection.csizeh) {
            theSelection.bHow[2] = true;
            theSelection.iCSize[2] = theSelection.csizeh;
        }
        if (iMouseX > theSelection.x - theSelection.csizeh && iMouseX < theSelection.x + theSelection.csizeh &&
            iMouseY > theSelection.y + theSelection.h-theSelection.csizeh && iMouseY < theSelection.y + theSelection.h + theSelection.csizeh) {
            theSelection.bHow[3] = true;
            theSelection.iCSize[3] = theSelection.csizeh;
        }
        // in case of dragging of resize cubes
        var iFW, iFH;
        if (theSelection.bDrag[0]) {
            var iFX = iMouseX - theSelection.px;
            var iFY = iMouseY - theSelection.py;
            iFW = theSelection.w + theSelection.x - iFX;
            iFH = theSelection.h + theSelection.y - iFY;
        }
        if (theSelection.bDrag[1]) {
            var iFX = theSelection.x;
            var iFY = iMouseY - theSelection.py;
            iFW = iMouseX - theSelection.px - iFX;
            iFH = theSelection.h + theSelection.y - iFY;
        }
        if (theSelection.bDrag[2]) {
            var iFX = theSelection.x;
            var iFY = theSelection.y;
            iFW = iMouseX - theSelection.px - iFX;
            iFH = iMouseY - theSelection.py - iFY;
        }
        if (theSelection.bDrag[3]) {
            var iFX = iMouseX - theSelection.px;
            var iFY = theSelection.y;
            iFW = theSelection.w + theSelection.x - iFX;
            iFH = iMouseY - theSelection.py - iFY;
        }
        if (iFW > theSelection.csizeh * 2 && iFH > theSelection.csizeh * 2) {
            theSelection.w = iFW;
            theSelection.h = iFH;
            theSelection.x = iFX;
            theSelection.y = iFY;
        }
        drawScene();
    });
    $('#selection').mousedown(function(e) { // binding mousedown event
        var canvasOffset = $(canvas).offset();
        iMouseX = Math.floor(e.pageX - canvasOffset.left);
        iMouseY = Math.floor(e.pageY - canvasOffset.top);
        theSelection.px = iMouseX - theSelection.x;
        theSelection.py = iMouseY - theSelection.y;
        if (theSelection.bHow[0]) {
            theSelection.px = iMouseX - theSelection.x;
            theSelection.py = iMouseY - theSelection.y;
        }
        if (theSelection.bHow[1]) {
            theSelection.px = iMouseX - theSelection.x - theSelection.w;
            theSelection.py = iMouseY - theSelection.y;
        }
        if (theSelection.bHow[2]) {
            theSelection.px = iMouseX - theSelection.x - theSelection.w;
            theSelection.py = iMouseY - theSelection.y - theSelection.h;
        }
        if (theSelection.bHow[3]) {
            theSelection.px = iMouseX - theSelection.x;
            theSelection.py = iMouseY - theSelection.y - theSelection.h;
        }
        if (iMouseX > theSelection.x + theSelection.csizeh && iMouseX < theSelection.x+theSelection.w - theSelection.csizeh &&
            iMouseY > theSelection.y + theSelection.csizeh && iMouseY < theSelection.y+theSelection.h - theSelection.csizeh) {
            theSelection.bDragAll = true;
        }
        for (i = 0; i < 4; i++) {
            if (theSelection.bHow[i]) {
                theSelection.bDrag[i] = true;
            }
        }
    });
    $('#selection').mouseup(function(e) { // binding mouseup event
        theSelection.bDragAll = false;
        for (i = 0; i < 4; i++) {
            theSelection.bDrag[i] = false;
        }
        theSelection.px = 0;
        theSelection.py = 0;
    });
    drawScene();
});

// Return selection values by post request to preview page
// Refresh preview page to update output image
function returnSelection(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/",
        data: {  // Adjust return values to reflect actual size
            "xPos": theSelection.x*scale,
            "yPos": theSelection.y*scale,
            "wSel": theSelection.w*scale,
            "hSel": theSelection.h*scale,
        },
        dataType: "json",
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
    document.location.href="/"
}